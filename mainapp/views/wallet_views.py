from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from mainapp.utils.common_utils import (
    login_required_admin, login_required_user,
    paginate_queryset, credit_wallet, get_wallet_balance
)
from mainapp.models import WalletRequest, WalletBalance, UserProfile
from mainapp.utils.validators import validate_image_file


@login_required_admin
def admin_wallet_requests(request):
    status  = request.GET.get('status', '')
    requests = WalletRequest.objects.select_related('user').all()
    if status:
        requests = requests.filter(status=status)
    page_obj = paginate_queryset(request, requests, per_page=15)
    return render(request, 'admin/wallet/wallet_requests.html', {
        'page_obj': page_obj,
        'selected_status': status,
    })


@login_required_admin
def approve_wallet(request, req_id):
    if request.method == 'POST':
        wr = get_object_or_404(WalletRequest, id=req_id)
        if wr.status != 'Pending':
            messages.warning(request, 'This request has already been processed.')
            return redirect('admin_wallet_requests')
        wr.status        = 'Approved'
        wr.remarks       = request.POST.get('remarks', '').strip() or None
        wr.approved_date = timezone.now()
        wr.save()
        credit_wallet(wr.user, wr.amount)
        messages.success(request, f'Wallet request of ₹{wr.amount} approved. Wallet credited.')
    return redirect('admin_wallet_requests')


@login_required_admin
def reject_wallet(request, req_id):
    if request.method == 'POST':
        wr = get_object_or_404(WalletRequest, id=req_id)
        if wr.status != 'Pending':
            messages.warning(request, 'This request has already been processed.')
            return redirect('admin_wallet_requests')
        wr.status  = 'Rejected'
        wr.remarks = request.POST.get('remarks', '').strip() or None
        wr.save()
        messages.success(request, f'Wallet request of ₹{wr.amount} rejected.')
    return redirect('admin_wallet_requests')


# ─── User Wallet Views ────────────────────────────────────────────────────────

@login_required_user
def user_wallet(request):
    user          = get_object_or_404(UserProfile, id=request.session['user_id'])
    balance       = get_wallet_balance(user)
    requests_qs   = WalletRequest.objects.filter(user=user)
    page_obj      = paginate_queryset(request, requests_qs, per_page=10)
    return render(request, 'user/wallet.html', {
        'balance':  balance,
        'page_obj': page_obj,
    })


@login_required_user
def submit_wallet_request(request):
    user = get_object_or_404(UserProfile, id=request.session['user_id'])

    if request.method == 'POST':
        utr    = request.POST.get('utr_number', '').strip()
        amount = request.POST.get('amount', '').strip()
        image  = request.FILES.get('receipt_image')

        if not utr or not amount or not image:
            messages.error(request, 'UTR number, amount, and receipt image are required.')
            return redirect('submit_wallet_request')

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Enter a valid positive amount.')
            return redirect('submit_wallet_request')

        try:
            validate_image_file(image)
        except ValidationError as e:
            messages.error(request, e.message)
            return redirect('submit_wallet_request')

        WalletRequest.objects.create(
            user          = user,
            utr_number    = utr,
            receipt_image = image,
            amount        = amount_val,
        )
        messages.success(request, 'Wallet top-up request submitted! Admin will review it shortly.')
        return redirect('user_wallet')

    return render(request, 'user/submit_wallet_request.html')


@login_required_admin
def admin_credit_wallet(request, user_id):
    """Admin manually credits a user's wallet."""
    if request.method != 'POST':
        return redirect('manage_users')

    user = get_object_or_404(UserProfile, id=user_id, is_admin=False)
    amount_str = request.POST.get('amount', '').strip()
    note       = request.POST.get('note', '').strip()

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messages.error(request, 'Enter a valid positive amount.')
        return redirect('view_user', user_id=user_id)

    credit_wallet(user, amount)
    messages.success(
        request,
        f'₹{amount:.0f} has been credited to {user.get_full_name()}\'s wallet.'
        + (f' Note: {note}' if note else '')
    )
    return redirect('view_user', user_id=user_id)
