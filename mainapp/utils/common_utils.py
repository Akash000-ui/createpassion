import uuid
from datetime import datetime
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


# ─── Order Number Generator ───────────────────────────────────────────────────

def generate_order_number():
    """Generate a unique order number: ORD-YYYYMMDD-XXXX"""
    date_str = datetime.now().strftime('%Y%m%d')
    unique   = str(uuid.uuid4()).replace('-', '').upper()[:6]
    return f'ORD-{date_str}-{unique}'


# ─── Decorators ───────────────────────────────────────────────────────────────

def login_required_user(view_func):
    """Redirect to login if user not in session."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, 'Please login to continue.')
            return redirect('user_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_admin(view_func):
    """Redirect to admin login if admin not in session."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            messages.warning(request, 'Admin access required.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def already_logged_in_user(view_func):
    """Redirect logged-in users away from login/register pages."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('user_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def already_logged_in_admin(view_func):
    """Redirect logged-in admin away from login page."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('admin_logged_in'):
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Wallet Helpers ───────────────────────────────────────────────────────────

def get_wallet_balance(user):
    """Return the user's current wallet balance, creating record if needed."""
    from mainapp.models import WalletBalance
    wallet, _ = WalletBalance.objects.get_or_create(user=user)
    return wallet.balance


def credit_wallet(user, amount):
    """Add amount to user's wallet."""
    from mainapp.models import WalletBalance
    wallet, _ = WalletBalance.objects.get_or_create(user=user)
    wallet.balance += amount
    wallet.save()


def debit_wallet(user, amount):
    """Deduct amount from user's wallet. Returns True on success, False if insufficient."""
    from mainapp.models import WalletBalance
    wallet, _ = WalletBalance.objects.get_or_create(user=user)
    if wallet.balance >= amount:
        wallet.balance -= amount
        wallet.save()
        return True
    return False


# ─── Cart Helpers ─────────────────────────────────────────────────────────────

def get_cart_count(user):
    """Return total cart item count for a user."""
    from mainapp.models import Cart
    return Cart.objects.filter(user=user).count()


# ─── Pagination Helper ────────────────────────────────────────────────────────

def paginate_queryset(request, queryset, per_page=12):
    """Return a Page object for the given queryset."""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page', 1)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
