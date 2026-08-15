import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core import signing
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse

from mainapp.models import UserProfile, WalletBalance, ProductCategory, Product
from mainapp.forms.auth_forms import (
    UserRegistrationForm, UserLoginForm,
    ForgotPasswordForm, ResetPasswordForm,
)
from mainapp.utils.common_utils import already_logged_in_user, login_required_user


logger = logging.getLogger(__name__)
PASSWORD_RESET_SALT = 'mainapp.password-reset'


# ─── Home Page ────────────────────────────────────────────────────────────────

def home(request):
    categories      = ProductCategory.objects.filter(status=True)[:8]
    featured        = Product.objects.filter(featured=True, stock__gt=0)[:8]
    trending        = Product.objects.filter(trending=True, stock__gt=0)[:8]
    latest          = Product.objects.filter(stock__gt=0).order_by('-created_at')[:8]

    cart_count = 0
    if request.session.get('user_id'):
        from mainapp.utils.common_utils import get_cart_count
        try:
            user = UserProfile.objects.get(id=request.session['user_id'])
            cart_count = get_cart_count(user)
        except UserProfile.DoesNotExist:
            pass

    context = {
        'categories': categories,
        'featured':   featured,
        'trending':   trending,
        'latest':     latest,
        'cart_count': cart_count,
    }
    return render(request, 'home.html', context)


# ─── User Registration ────────────────────────────────────────────────────────

@already_logged_in_user
def user_register(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email  = form.cleaned_data['email'].lower().strip()
            mobile = form.cleaned_data['mobile'].strip()

            if UserProfile.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
            elif UserProfile.objects.filter(mobile=mobile).exists():
                messages.error(request, 'An account with this mobile number already exists.')
            else:
                user = UserProfile(
                    first_name = form.cleaned_data['first_name'].strip(),
                    last_name  = form.cleaned_data['last_name'].strip(),
                    email      = email,
                    mobile     = mobile,
                    password   = make_password(form.cleaned_data['password']),
                )
                user.save()
                # Create wallet for the user
                WalletBalance.objects.create(user=user, balance=0)
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('user_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    return render(request, 'user/register.html', {'form': form})


# ─── User Login ───────────────────────────────────────────────────────────────

@already_logged_in_user
def user_login(request):
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier'].strip()
            password   = form.cleaned_data['password']

            # Try email first, then member_id
            user = None
            try:
                user = UserProfile.objects.get(email__iexact=identifier, is_admin=False)
            except UserProfile.DoesNotExist:
                try:
                    user = UserProfile.objects.get(member_id__iexact=identifier, is_admin=False)
                except UserProfile.DoesNotExist:
                    pass

            if user is None:
                messages.error(request, 'Invalid email / Member ID or password.')
            elif not user.is_active:
                messages.error(request, 'Your account has been deactivated. Please contact support.')
            elif check_password(password, user.password):
                request.session['user_id']    = user.id
                request.session['user_name']  = user.first_name
                request.session['user_email'] = user.email or ''
                request.session['member_id']  = user.member_id or ''
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid email / Member ID or password.')
        else:
            messages.error(request, 'Please fill in all fields correctly.')

    return render(request, 'user/login.html', {'form': form})


# ─── User Logout ──────────────────────────────────────────────────────────────

def user_logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('user_login')


# ─── Admin Login ──────────────────────────────────────────────────────────────

def admin_login(request):
    if request.session.get('admin_logged_in'):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        email    = request.POST.get('email', '').lower().strip()
        password = request.POST.get('password', '')

        try:
            admin = UserProfile.objects.get(email=email, is_admin=True)
            if check_password(password, admin.password):
                request.session['admin_logged_in'] = True
                request.session['admin_name']      = admin.first_name
                request.session['admin_id']        = admin.id
                messages.success(request, f'Welcome, {admin.first_name}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'admin/admin_login.html')


# ─── Admin Logout ─────────────────────────────────────────────────────────────

def admin_logout(request):
    keys_to_clear = ['admin_logged_in', 'admin_name', 'admin_id']
    for key in keys_to_clear:
        request.session.pop(key, None)
    messages.success(request, 'Logged out from admin panel.')
    return redirect('admin_login')


# ─── Forgot Password ─────────────────────────────────────────────────────────

@already_logged_in_user
def forgot_password(request):
    """Send a password reset link to a registered user's email."""
    form = ForgotPasswordForm()

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
            user = UserProfile.objects.filter(
                email__iexact=email,
                is_admin=False,
                is_active=True,
            ).first()

            if user:
                token = signing.dumps({'user_id': user.id}, salt=PASSWORD_RESET_SALT)
                reset_url = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'token': token})
                )
                subject = 'Reset your CREATE PASSION password'
                message = (
                    f'Hello {user.first_name},\n\n'
                    'We received a request to reset your CREATE PASSION account password.\n'
                    f'Use this link to set a new password:\n{reset_url}\n\n'
                    f'This link expires in {settings.PASSWORD_RESET_TIMEOUT // 60} minutes.\n'
                    'If you did not request this, you can ignore this email.\n\n'
                    'CREATE PASSION'
                )
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception:
                    logger.exception('Failed to send password reset email to user_id=%s', user.id)
                    messages.error(request, 'Unable to send reset email right now. Please try again later.')
                    return redirect('forgot_password')

            messages.success(
                request,
                'If an active account exists for that email, a password reset link has been sent.',
            )
            return redirect('user_login')

    return render(request, 'user/forgot_password.html', {'form': form})


# ─── Reset Password ───────────────────────────────────────────────────────────

@already_logged_in_user
def reset_password(request, token=None):
    """Set a new password using a signed reset token."""
    if not token:
        messages.warning(request, 'Please use the reset link sent to your email.')
        return redirect('forgot_password')

    try:
        data = signing.loads(
            token,
            salt=PASSWORD_RESET_SALT,
            max_age=settings.PASSWORD_RESET_TIMEOUT,
        )
        user = UserProfile.objects.get(
            id=data.get('user_id'),
            is_admin=False,
            is_active=True,
        )
    except signing.SignatureExpired:
        messages.error(request, 'This password reset link has expired. Please request a new one.')
        return redirect('forgot_password')
    except (signing.BadSignature, UserProfile.DoesNotExist, TypeError, ValueError):
        messages.error(request, 'Invalid password reset link. Please request a new one.')
        return redirect('forgot_password')

    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.password = make_password(form.cleaned_data['new_password'])
            user.save(update_fields=['password', 'updated_at'])
            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('user_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    return render(request, 'user/reset_password.html', {'form': form, 'email': user.email})
