from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from mainapp.utils.common_utils import login_required_admin
from mainapp.models import (
    UserProfile, Product, ProductCategory, Order,
    WalletRequest, KYC, Event, EventRegistration
)


@login_required_admin
def admin_dashboard(request):
    total_users     = UserProfile.objects.filter(is_admin=False).count()
    active_users    = UserProfile.objects.filter(is_admin=False, is_active=True).count()
    total_products  = Product.objects.count()
    total_categories = ProductCategory.objects.count()
    total_orders    = Order.objects.count()
    total_revenue   = Order.objects.filter(status='Delivered').aggregate(
                        rev=Sum('total_amount'))['rev'] or 0
    pending_wallet  = WalletRequest.objects.filter(status='Pending').count()
    pending_kyc     = KYC.objects.filter(approval_status='Pending').count()
    total_events    = Event.objects.count()

    recent_orders   = Order.objects.select_related('user').order_by('-order_date')[:8]
    recent_users    = UserProfile.objects.filter(is_admin=False).order_by('-joining_date')[:8]

    order_status_counts = {
        'Pending':   Order.objects.filter(status='Pending').count(),
        'Confirmed': Order.objects.filter(status='Confirmed').count(),
        'Shipped':   Order.objects.filter(status='Shipped').count(),
        'Delivered': Order.objects.filter(status='Delivered').count(),
        'Cancelled': Order.objects.filter(status='Cancelled').count(),
    }

    context = {
        'total_users':      total_users,
        'active_users':     active_users,
        'total_products':   total_products,
        'total_categories': total_categories,
        'total_orders':     total_orders,
        'total_revenue':    total_revenue,
        'pending_wallet':   pending_wallet,
        'pending_kyc':      pending_kyc,
        'total_events':     total_events,
        'recent_orders':    recent_orders,
        'recent_users':     recent_users,
        'order_status_counts': order_status_counts,
    }
    return render(request, 'admin/admin_dashboard.html', context)
