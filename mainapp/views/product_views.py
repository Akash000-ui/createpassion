from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import login_required_admin, paginate_queryset
from django.core.exceptions import ValidationError
from mainapp.utils.validators import validate_image_file
from mainapp.models import ProductCategory, Product, ProductImage, ProductSize


# ─────────────────────── CATEGORIES ───────────────────────

@login_required_admin
def manage_categories(request):
    query = request.GET.get('q', '').strip()
    cats  = ProductCategory.objects.all().order_by('category_name')
    if query:
        cats = cats.filter(category_name__icontains=query)
    page_obj = paginate_queryset(request, cats, per_page=15)
    return render(request, 'admin/products/categories.html', {
        'page_obj': page_obj, 'query': query
    })


@login_required_admin
def add_category(request):
    if request.method == 'POST':
        name  = request.POST.get('category_name', '').strip()
        desc  = request.POST.get('description', '').strip()
        image = request.FILES.get('category_image')

        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('add_category')
        if ProductCategory.objects.filter(category_name__iexact=name).exists():
            messages.error(request, 'A category with this name already exists.')
            return redirect('add_category')

        cat = ProductCategory(category_name=name, description=desc or None)
        if image:
            try:
                validate_image_file(image)
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect('add_category')
            cat.category_image = image
        cat.save()
        messages.success(request, f'Category "{name}" added successfully.')
        return redirect('manage_categories')

    return render(request, 'admin/products/add_category.html')


@login_required_admin
def edit_category(request, cat_id):
    cat = get_object_or_404(ProductCategory, id=cat_id)
    if request.method == 'POST':
        name   = request.POST.get('category_name', '').strip()
        desc   = request.POST.get('description', '').strip()
        status = request.POST.get('status') == 'on'
        image  = request.FILES.get('category_image')

        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('edit_category', cat_id=cat_id)
        if ProductCategory.objects.filter(category_name__iexact=name).exclude(id=cat_id).exists():
            messages.error(request, 'Another category with this name already exists.')
            return redirect('edit_category', cat_id=cat_id)

        cat.category_name = name
        cat.description   = desc or None
        cat.status        = status
        if image:
            try:
                validate_image_file(image)
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect('edit_category', cat_id=cat_id)
            cat.category_image = image
        cat.save()
        messages.success(request, f'Category "{name}" updated successfully.')
        return redirect('manage_categories')

    return render(request, 'admin/products/edit_category.html', {'cat': cat})


@login_required_admin
def delete_category(request, cat_id):
    if request.method == 'POST':
        cat = get_object_or_404(ProductCategory, id=cat_id)
        name = cat.category_name
        cat.delete()
        messages.success(request, f'Category "{name}" deleted.')
    return redirect('manage_categories')


# ─────────────────────── PRODUCTS ───────────────────────

SIZE_LIST = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '28', '30', '32', '34', '36', '38', '40']
PRODUCT_SECTIONS = ['Men', 'Women', 'Unisex']  # Accessories hidden from UI for now.


@login_required_admin
def manage_products(request):
    query    = request.GET.get('q', '').strip()
    cat_id   = request.GET.get('cat', '')
    products = Product.objects.select_related('category').all()
    if query:
        products = products.filter(name__icontains=query)
    if cat_id:
        products = products.filter(category_id=cat_id)
    page_obj   = paginate_queryset(request, products, per_page=15)
    categories = ProductCategory.objects.filter(status=True)
    return render(request, 'admin/products/products.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'selected_cat': cat_id,
    })


@login_required_admin
def add_product(request):
    categories = ProductCategory.objects.filter(status=True)
    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        cat_id      = request.POST.get('category')
        brand       = request.POST.get('brand', '').strip()
        model_no    = request.POST.get('model_no', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price')
        discount    = request.POST.get('discount_percentage', '0')
        stock       = request.POST.get('stock', '0')
        color       = request.POST.get('color', '').strip()
        gender      = request.POST.get('gender', 'Unisex')
        if gender not in PRODUCT_SECTIONS:
            gender = 'Unisex'
        featured    = request.POST.get('featured') == 'on'
        trending    = request.POST.get('trending') == 'on'
        main_image  = request.FILES.get('main_image')
        sizes       = request.POST.getlist('sizes')

        if not all([name, price, main_image]):
            messages.error(request, 'Name, price, and main image are required.')
            return render(request, 'admin/products/add_product.html', {'categories': categories, 'size_list': SIZE_LIST})

        try:
            validate_image_file(main_image)
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request, 'admin/products/add_product.html', {'categories': categories, 'size_list': SIZE_LIST})

        category = ProductCategory.objects.filter(id=cat_id).first() if cat_id else None
        product  = Product(
            name=name, category=category, brand=brand or None,
            model_no=model_no or None, description=description or None,
            price=price, discount_percentage=discount or 0, stock=stock or 0,
            color=color or None, gender=gender, featured=featured, trending=trending,
            main_image=main_image,
        )
        product.save()

        # Sizes
        for size in sizes:
            if size in SIZE_LIST:
                ProductSize.objects.get_or_create(product=product, size=size)

        for img in request.FILES.getlist('gallery_images'):
            try:
                validate_image_file(img)
                ProductImage.objects.create(product=product, image=img)
            except ValidationError:
                pass

        messages.success(request, f'Product "{name}" added successfully.')
        return redirect('manage_products')

    return render(request, 'admin/products/add_product.html', {
        'categories': categories, 'size_list': SIZE_LIST
    })


@login_required_admin
def edit_product(request, prod_id):
    product    = get_object_or_404(Product, id=prod_id)
    categories = ProductCategory.objects.filter(status=True)
    current_sizes = list(product.sizes.values_list('size', flat=True))

    if request.method == 'POST':
        name        = request.POST.get('name', '').strip()
        cat_id      = request.POST.get('category')
        brand       = request.POST.get('brand', '').strip()
        model_no    = request.POST.get('model_no', '').strip()
        description = request.POST.get('description', '').strip()
        price       = request.POST.get('price')
        discount    = request.POST.get('discount_percentage', '0')
        stock       = request.POST.get('stock', '0')
        color       = request.POST.get('color', '').strip()
        gender      = request.POST.get('gender', 'Unisex')
        if gender not in PRODUCT_SECTIONS:
            gender = 'Unisex'
        featured    = request.POST.get('featured') == 'on'
        trending    = request.POST.get('trending') == 'on'
        main_image  = request.FILES.get('main_image')
        sizes       = request.POST.getlist('sizes')
        del_images  = request.POST.getlist('delete_images')

        if not name or not price:
            messages.error(request, 'Name and price are required.')
            return render(request, 'admin/products/edit_product.html', {
                'product': product, 'categories': categories,
                'size_list': SIZE_LIST, 'current_sizes': current_sizes
            })

        product.name        = name
        product.category    = ProductCategory.objects.filter(id=cat_id).first() if cat_id else None
        product.brand       = brand or None
        product.model_no    = model_no or None
        product.description = description or None
        product.price       = price
        product.discount_percentage = discount or 0
        product.stock       = stock or 0
        product.color       = color or None
        product.gender      = gender
        product.featured    = featured
        product.trending    = trending

        if main_image:
            try:
                validate_image_file(main_image)
            except ValidationError as e:
                messages.error(request, e.message)
                return render(request, 'admin/products/edit_product.html', {
                    'product': product, 'categories': categories,
                    'size_list': SIZE_LIST, 'current_sizes': current_sizes
                })
            product.main_image = main_image
        product.save()

        # Update sizes
        ProductSize.objects.filter(product=product).delete()
        for size in sizes:
            if size in SIZE_LIST:
                ProductSize.objects.get_or_create(product=product, size=size)

        # Delete gallery images
        if del_images:
            ProductImage.objects.filter(id__in=del_images, product=product).delete()

        # Add new gallery images
        for img in request.FILES.getlist('gallery_images'):
            try:
                validate_image_file(img)
                ProductImage.objects.create(product=product, image=img)
            except ValidationError:
                pass

        messages.success(request, f'Product "{name}" updated successfully.')
        return redirect('manage_products')

    return render(request, 'admin/products/edit_product.html', {
        'product': product,
        'categories': categories,
        'size_list': SIZE_LIST,
        'current_sizes': current_sizes,
    })


@login_required_admin
def delete_product(request, prod_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=prod_id)
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
    return redirect('manage_products')


@login_required_admin
def toggle_featured(request, prod_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=prod_id)
        product.featured = not product.featured
        product.save()
        state = 'featured' if product.featured else 'unfeatured'
        messages.success(request, f'"{product.name}" marked as {state}.')
    return redirect('manage_products')


@login_required_admin
def toggle_trending(request, prod_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=prod_id)
        product.trending = not product.trending
        product.save()
        state = 'trending' if product.trending else 'not trending'
        messages.success(request, f'"{product.name}" marked as {state}.')
    return redirect('manage_products')
