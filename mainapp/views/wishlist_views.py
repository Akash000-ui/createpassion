from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from mainapp.models import Wishlist, Product, UserProfile
from mainapp.utils.common_utils import login_required_user
from mainapp.views.browsing_views import get_cart_count_safe
from django.shortcuts import render


def _get_user(request):
    return get_object_or_404(UserProfile, id=request.session['user_id'])


# ─── Wishlist Page ────────────────────────────────────────────────────────────

@login_required_user
def view_wishlist(request):
    user  = _get_user(request)
    items = Wishlist.objects.filter(user=user).select_related('product')

    wishlist_ids = list(items.values_list('product_id', flat=True))

    context = {
        'items':       items,
        'wishlist_ids': wishlist_ids,
        'cart_count':  get_cart_count_safe(request),
    }
    return render(request, 'user/wishlist.html', context)


# ─── Toggle Wishlist ──────────────────────────────────────────────────────────

@login_required_user
def toggle_wishlist(request):
    if request.method != 'POST':
        return redirect('view_wishlist')

    user       = _get_user(request)
    product_id = request.POST.get('product_id')
    product    = get_object_or_404(Product, id=product_id)

    existing = Wishlist.objects.filter(user=user, product=product).first()
    if existing:
        existing.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        Wishlist.objects.create(user=user, product=product)
        messages.success(request, f'"{product.name}" added to wishlist!')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


# ─── Move to Cart ─────────────────────────────────────────────────────────────

@login_required_user
def move_to_cart(request, item_id):
    if request.method != 'POST':
        return redirect('view_wishlist')

    user  = _get_user(request)
    witem = get_object_or_404(Wishlist, id=item_id, user=user)
    product = witem.product

    if not product.is_in_stock():
        messages.error(request, f'"{product.name}" is out of stock.')
        return redirect('view_wishlist')

    from mainapp.models import Cart
    cart_item, created = Cart.objects.get_or_create(
        user=user, product=product, size=None,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    witem.delete()
    messages.success(request, f'"{product.name}" moved to cart!')
    return redirect('view_wishlist')
