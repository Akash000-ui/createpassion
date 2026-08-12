from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import login_required_admin, login_required_user, paginate_queryset
from mainapp.models import BankDetails, UserProfile


@login_required_admin
def admin_bank_list(request):
    status  = request.GET.get('status', '')
    bank_qs = BankDetails.objects.select_related('user').order_by('-submitted_at')
    if status:
        bank_qs = bank_qs.filter(approval_status=status)
    page_obj = paginate_queryset(request, bank_qs, per_page=15)
    return render(request, 'admin/bank/bank_list.html', {
        'page_obj': page_obj,
        'selected_status': status,
    })


@login_required_admin
def admin_bank_detail(request, bank_id):
    bank = get_object_or_404(BankDetails, id=bank_id)
    return render(request, 'admin/bank/bank_detail.html', {'bank': bank})


@login_required_admin
def approve_bank(request, bank_id):
    if request.method == 'POST':
        bank = get_object_or_404(BankDetails, id=bank_id)
        bank.approval_status = 'Approved'
        bank.remarks = request.POST.get('remarks', '').strip() or None
        bank.save()
        messages.success(request, f'Bank details for {bank.user.get_full_name()} approved.')
    return redirect('admin_bank_detail', bank_id=bank_id)


@login_required_admin
def reject_bank(request, bank_id):
    if request.method == 'POST':
        bank = get_object_or_404(BankDetails, id=bank_id)
        bank.approval_status = 'Rejected'
        bank.remarks = request.POST.get('remarks', '').strip() or None
        bank.save()
        messages.success(request, f'Bank details for {bank.user.get_full_name()} rejected.')
    return redirect('admin_bank_detail', bank_id=bank_id)


# ─── User Bank Views ──────────────────────────────────────────────────────────

@login_required_user
def user_bank_submit(request):
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    try:
        bank = BankDetails.objects.get(user=user)
    except BankDetails.DoesNotExist:
        bank = None

    if request.method == 'POST':
        holder_name    = request.POST.get('account_holder_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        account_type   = request.POST.get('account_type', 'Savings')
        ifsc_code      = request.POST.get('ifsc_code', '').strip().upper()
        bank_name      = request.POST.get('bank_name', '').strip()
        branch_name    = request.POST.get('branch_name', '').strip()

        errors = []
        if not holder_name:
            errors.append('Account Holder Name is required.')
        if not account_number:
            errors.append('Account Number is required.')
        if not ifsc_code:
            errors.append('IFSC Code is required.')
        if not bank_name:
            errors.append('Bank Name is required.')
        if account_type not in ['Savings', 'Current']:
            errors.append('Invalid account type.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'user/bank_submit.html', {'bank': bank})

        if bank:
            bank.account_holder_name = holder_name
            bank.account_number      = account_number
            bank.account_type        = account_type
            bank.ifsc_code           = ifsc_code
            bank.bank_name           = bank_name
            bank.branch_name         = branch_name
            bank.approval_status     = 'Pending'
            bank.remarks             = None
            bank.save()
            messages.success(request, 'Bank details updated and re-submitted for review.')
        else:
            BankDetails.objects.create(
                user                = user,
                account_holder_name = holder_name,
                account_number      = account_number,
                account_type        = account_type,
                ifsc_code           = ifsc_code,
                bank_name           = bank_name,
                branch_name         = branch_name,
            )
            messages.success(request, 'Bank details submitted! Admin will review shortly.')
        return redirect('user_bank_detail')

    return render(request, 'user/bank_submit.html', {'bank': bank})


@login_required_user
def user_bank_detail(request):
    """Read-only view of the user's submitted bank details."""
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    try:
        bank = BankDetails.objects.get(user=user)
    except BankDetails.DoesNotExist:
        messages.info(request, 'You have not submitted bank details yet. Please fill the form below.')
        return redirect('user_bank_submit')
    return render(request, 'user/bank_detail.html', {'bank': bank})
