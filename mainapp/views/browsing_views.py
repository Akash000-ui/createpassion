from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from mainapp.models import (
    Product, ProductCategory, ProductImage, ProductSize,
    Rating, Review, Cart, Wishlist
)
from mainapp.utils.common_utils import login_required_user, paginate_queryset


# ─── Shop / Product Listing ───────────────────────────────────────────────────

def shop(request):
    products = Product.objects.filter(stock__gt=0).select_related('category')

    # Filters
    category_id = request.GET.get('category')
    gender      = request.GET.get('gender')
    color       = request.GET.get('color')
    size        = request.GET.get('size')
    sort        = request.GET.get('sort', 'latest')
    q           = request.GET.get('q', '').strip()

    colors = (
        Product.objects
        .filter(stock__gt=0)
        .exclude(color__isnull=True)
        .exclude(color='')
        .order_by('color')
        .values_list('color', flat=True)
        .distinct()
    )
    sizes = ProductSize.SIZE_CHOICES

    if q:
        products = products.filter(name__icontains=q)
    if category_id:
        products = products.filter(category_id=category_id)
    if gender:
        products = products.filter(gender=gender)
    if color:
        products = products.filter(color__iexact=color)
    if size:
        products = products.filter(sizes__size=size)

    sort_map = {
        'latest':      '-created_at',
        'price_asc':   'price',
        'price_desc':  '-price',
        'name':        'name',
    }
    products = products.distinct().order_by(sort_map.get(sort, '-created_at'))

    # Wishlist IDs for logged-in user
    wishlist_ids = []
    if request.session.get('user_id'):
        wishlist_ids = list(
            Wishlist.objects.filter(user_id=request.session['user_id'])
            .values_list('product_id', flat=True)
        )

    page_obj = paginate_queryset(request, products, per_page=12)

    context = {
        'page_obj':    page_obj,
        'categories':  ProductCategory.objects.filter(status=True),
        'colors':      colors,
        'sizes':       sizes,
        'wishlist_ids': wishlist_ids,
        'selected_category': category_id,
        'selected_gender':   gender,
        'selected_color':    color,
        'selected_size':     size,
        'selected_sort':     sort,
        'q':           q,
        'cart_count':  get_cart_count_safe(request),
    }
    return render(request, 'user/shop.html', context)


def product_detail(request, prod_id):
    product    = get_object_or_404(Product, id=prod_id)
    images     = product.images.all()
    sizes      = product.sizes.values_list('size', flat=True)
    reviews    = product.reviews.select_related('user').all()
    related    = Product.objects.filter(
        category=product.category, stock__gt=0
    ).exclude(id=prod_id)[:4]

    user_rating = None
    user_review = None
    wishlist_ids = []
    in_cart = False

    if request.session.get('user_id'):
        user_id = request.session['user_id']
        try:
            user_rating = Rating.objects.get(user_id=user_id, product=product).rating
        except Rating.DoesNotExist:
            pass
        try:
            user_review = Review.objects.get(user_id=user_id, product=product).review
        except Review.DoesNotExist:
            pass
        wishlist_ids = list(
            Wishlist.objects.filter(user_id=user_id).values_list('product_id', flat=True)
        )
        in_cart = Cart.objects.filter(user_id=user_id, product=product).exists()

    context = {
        'product':      product,
        'images':       images,
        'sizes':        list(sizes),
        'reviews':      reviews,
        'related':      related,
        'user_rating':  user_rating,
        'user_review':  user_review,
        'wishlist_ids': wishlist_ids,
        'in_cart':      in_cart,
        'avg_rating':   product.average_rating(),
        'rating_count': product.ratings.count(),
        'cart_count':   get_cart_count_safe(request),
    }
    return render(request, 'user/product_detail.html', context)


@login_required_user
def submit_review(request, prod_id):
    """Submit or update a rating + review for a product."""
    if request.method != 'POST':
        return redirect('product_detail', prod_id=prod_id)

    product = get_object_or_404(Product, id=prod_id)
    user_id = request.session['user_id']
    from mainapp.models import UserProfile
    user = get_object_or_404(UserProfile, id=user_id)

    rating_val = request.POST.get('rating', '').strip()
    review_text = request.POST.get('review', '').strip()

    if rating_val:
        try:
            rating_int = int(rating_val)
            if 1 <= rating_int <= 5:
                Rating.objects.update_or_create(
                    user=user, product=product,
                    defaults={'rating': rating_int}
                )
        except ValueError:
            pass

    if review_text:
        Review.objects.update_or_create(
            user=user, product=product,
            defaults={'review': review_text}
        )

    messages.success(request, 'Your review has been submitted.')
    return redirect('product_detail', prod_id=prod_id)


# ─── Helper ──────────────────────────────────────────────────────────────────

def get_cart_count_safe(request):
    if request.session.get('user_id'):
        try:
            return Cart.objects.filter(user_id=request.session['user_id']).count()
        except Exception:
            return 0
    return 0
