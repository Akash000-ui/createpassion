from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import (
    login_required_admin, login_required_user,
    paginate_queryset, generate_order_number, debit_wallet,
    calculate_cart_totals
)
from mainapp.models import Order, OrderItem, Cart, UserProfile
from mainapp.utils.pdf_utils import build_order_invoice


@login_required_admin
def admin_orders(request):
    status = request.GET.get('status', '')
    query  = request.GET.get('q', '').strip()

    orders = Order.objects.select_related('user').all()
    if status:
        orders = orders.filter(status=status)
    if query:
        orders = orders.filter(order_number__icontains=query) | \
                 Order.objects.select_related('user').filter(
                     user__first_name__icontains=query
                 ) | Order.objects.select_related('user').filter(
                     user__email__icontains=query
                 )
        orders = orders.distinct()

    page_obj = paginate_queryset(request, orders, per_page=15)
    status_choices = ['Pending', 'Confirmed', 'Packed', 'Shipped', 'Delivered', 'Cancelled']
    return render(request, 'admin/orders/admin_orders.html', {
        'page_obj': page_obj,
        'query': query,
        'selected_status': status,
        'status_choices': status_choices,
    })


@login_required_admin
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order).select_related('product')
    status_choices = ['Pending', 'Confirmed', 'Packed', 'Shipped', 'Delivered', 'Cancelled']
    return render(request, 'admin/orders/admin_order_detail.html', {
        'order': order,
        'items': items,
        'status_choices': status_choices,
    })


@login_required_admin
def update_order_status(request, order_id):
    if request.method == 'POST':
        order  = get_object_or_404(Order, id=order_id)
        status = request.POST.get('status')
        valid  = ['Pending', 'Confirmed', 'Packed', 'Shipped', 'Delivered', 'Cancelled']
        if status in valid:
            order.status = status
            order.save()
            messages.success(request, f'Order #{order.order_number} status updated to {status}.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('admin_order_detail', order_id=order_id)


# ─── User Order Views ─────────────────────────────────────────────────────────

@login_required_user
def checkout(request):
    user      = get_object_or_404(UserProfile, id=request.session['user_id'])
    cart_items = Cart.objects.filter(user=user).select_related('product')

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('view_cart')

    totals = calculate_cart_totals(cart_items)
    subtotal = totals['subtotal']
    delivery = totals['delivery']
    total    = totals['total']

    # Wallet balance
    from mainapp.utils.common_utils import get_wallet_balance
    wallet_balance = get_wallet_balance(user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'Wallet')
        if payment_method not in ('Wallet',):
            messages.error(request, 'Invalid payment method.')
            return render(request, 'user/checkout.html', {
                'cart_items': cart_items,
                'subtotal': subtotal, 'gross_total': totals['gross_total'],
                'tax_total': totals['tax_total'], 'delivery': delivery, 'total': total,
                'wallet_balance': wallet_balance, 'user': user,
            })

        # Build delivery address from form
        name      = request.POST.get('full_name', '').strip()
        mobile    = request.POST.get('mobile', '').strip()
        address   = request.POST.get('address', '').strip()
        city      = request.POST.get('city', '').strip()
        state     = request.POST.get('state', '').strip()
        pincode   = request.POST.get('pincode', '').strip()
        country   = request.POST.get('country', 'India').strip()

        if not all([name, mobile, address, city, state, pincode]):
            messages.error(request, 'Please fill all delivery address fields.')
            return render(request, 'user/checkout.html', {
                'cart_items': cart_items,
                'subtotal': subtotal, 'gross_total': totals['gross_total'],
                'tax_total': totals['tax_total'], 'delivery': delivery, 'total': total,
                'wallet_balance': wallet_balance, 'user': user,
            })

        delivery_address = (
            f"{name}\n{mobile}\n{address}\n{city}, {state} - {pincode}\n{country}"
        )

        # Wallet payment check
        if payment_method == 'Wallet':
            if wallet_balance < total:
                messages.error(request, f'Insufficient wallet balance. Available: ₹{wallet_balance}, Required: ₹{total}')
                return render(request, 'user/checkout.html', {
                    'cart_items': cart_items,
                    'subtotal': subtotal, 'gross_total': totals['gross_total'],
                    'tax_total': totals['tax_total'], 'delivery': delivery, 'total': total,
                    'wallet_balance': wallet_balance, 'user': user,
                })
            debit_wallet(user, total)

        # Create Order
        order = Order.objects.create(
            user             = user,
            order_number     = generate_order_number(),
            delivery_address = delivery_address,
            subtotal         = subtotal,
            delivery_charge  = delivery,
            total_amount     = total,
            status           = 'Pending',
        )

        # Create OrderItems & reduce stock
        for item in cart_items:
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                size     = item.size,
                quantity = item.quantity,
                price    = item.product.get_discounted_price(),
            )
            # Reduce stock
            product = item.product
            product.stock = max(0, product.stock - item.quantity)
            product.save(update_fields=['stock'])

        # Clear cart
        cart_items.delete()

        messages.success(request, f'Order #{order.order_number} placed successfully!')
        return redirect('user_order_detail', order_id=order.id)

    return render(request, 'user/checkout.html', {
        'cart_items':     cart_items,
        'subtotal':       subtotal,
        'gross_total':    totals['gross_total'],
        'tax_total':      totals['tax_total'],
        'delivery':       delivery,
        'total':          total,
        'wallet_balance': wallet_balance,
        'user':           user,
    })


@login_required_user
def user_orders(request):
    user   = get_object_or_404(UserProfile, id=request.session['user_id'])
    status = request.GET.get('status', '')
    orders = Order.objects.filter(user=user)
    if status:
        orders = orders.filter(status=status)
    page_obj = paginate_queryset(request, orders, per_page=10)
    return render(request, 'user/my_orders.html', {
        'page_obj':       page_obj,
        'selected_status': status,
        'status_choices': ['Pending', 'Confirmed', 'Packed', 'Shipped', 'Delivered', 'Cancelled'],
    })


@login_required_user
def user_order_detail(request, order_id):
    user  = get_object_or_404(UserProfile, id=request.session['user_id'])
    order = get_object_or_404(Order, id=order_id, user=user)
    items = OrderItem.objects.filter(order=order).select_related('product')
    return render(request, 'user/order_detail.html', {
        'order': order,
        'items': items,
    })


@login_required_user
def download_invoice(request, order_id):
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    order = get_object_or_404(Order, id=order_id, user=user)
    items = OrderItem.objects.filter(order=order).select_related('product')
    pdf = build_order_invoice(order, items)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="invoice-{order.order_number}.pdf"'
    )
    return response


@login_required_user
def cancel_order(request, order_id):
    if request.method != 'POST':
        return redirect('user_orders')

    user  = get_object_or_404(UserProfile, id=request.session['user_id'])
    order = get_object_or_404(Order, id=order_id, user=user)

    cancellable = ['Pending', 'Confirmed']
    if order.status not in cancellable:
        messages.error(request, f'Order cannot be cancelled at "{order.status}" stage.')
        return redirect('user_order_detail', order_id=order_id)

    order.status = 'Cancelled'
    order.save()
    messages.success(request, f'Order #{order.order_number} has been cancelled.')
    return redirect('user_order_detail', order_id=order_id)
