from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages

from mainapp.models import Cart, Product, UserProfile
from mainapp.utils.common_utils import login_required_user


def _get_user(request):
    return get_object_or_404(UserProfile, id=request.session['user_id'])


def _cart_count(user):
    return Cart.objects.filter(user=user).count()


# ─── View Cart ────────────────────────────────────────────────────────────────

@login_required_user
def view_cart(request):
    user  = _get_user(request)
    items = Cart.objects.filter(user=user).select_related('product')

    subtotal = sum(item.get_item_total() for item in items)
    delivery = 0 if subtotal >= 999 else 60
    total    = subtotal + delivery

    context = {
        'items':      items,
        'subtotal':   subtotal,
        'delivery':   delivery,
        'total':      total,
        'cart_count': items.count(),
    }
    return render(request, 'user/cart.html', context)


# ─── Add to Cart ──────────────────────────────────────────────────────────────

@login_required_user
def add_to_cart(request):
    if request.method != 'POST':
        return redirect('shop')

    user       = _get_user(request)
    product_id = request.POST.get('product_id')
    size       = request.POST.get('size', '').strip() or None
    quantity   = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)

    if not product.is_in_stock():
        messages.error(request, 'This product is out of stock.')
        return redirect('product_detail', prod_id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=user, product=product, size=size,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'"{product.name}" quantity updated in cart.')
    else:
        messages.success(request, f'"{product.name}" added to cart!')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


# ─── Update Cart Item ─────────────────────────────────────────────────────────

@login_required_user
def update_cart(request, item_id):
    if request.method != 'POST':
        return redirect('view_cart')

    user      = _get_user(request)
    cart_item = get_object_or_404(Cart, id=item_id, user=user)
    action    = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, 'Item removed from cart.')
            return redirect('view_cart')

    return redirect('view_cart')


# ─── Remove from Cart ─────────────────────────────────────────────────────────

@login_required_user
def remove_from_cart(request, item_id):
    user      = _get_user(request)
    cart_item = get_object_or_404(Cart, id=item_id, user=user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


# ─── Clear Cart ───────────────────────────────────────────────────────────────

@login_required_user
def clear_cart(request):
    if request.method == 'POST':
        user = _get_user(request)
        Cart.objects.filter(user=user).delete()
        messages.success(request, 'Cart cleared.')
    return redirect('view_cart')
