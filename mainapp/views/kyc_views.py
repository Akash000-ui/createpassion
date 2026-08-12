from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import login_required_admin, login_required_user, paginate_queryset
from mainapp.models import KYC, UserProfile
from mainapp.utils.validators import validate_kyc_image


@login_required_admin
def admin_kyc_list(request):
    status  = request.GET.get('status', '')
    kyc_qs  = KYC.objects.select_related('user').order_by('-submitted_at')
    if status:
        kyc_qs = kyc_qs.filter(approval_status=status)
    page_obj = paginate_queryset(request, kyc_qs, per_page=15)
    return render(request, 'admin/kyc/kyc_list.html', {
        'page_obj': page_obj,
        'selected_status': status,
    })


@login_required_admin
def admin_kyc_detail(request, kyc_id):
    kyc = get_object_or_404(KYC, id=kyc_id)
    return render(request, 'admin/kyc/kyc_detail.html', {'kyc': kyc})


@login_required_admin
def approve_kyc(request, kyc_id):
    if request.method == 'POST':
        kyc = get_object_or_404(KYC, id=kyc_id)
        kyc.approval_status = 'Approved'
        kyc.remarks = request.POST.get('remarks', '').strip() or None
        kyc.save()
        messages.success(request, f'KYC for {kyc.user.get_full_name()} approved.')
    return redirect('admin_kyc_detail', kyc_id=kyc_id)


@login_required_admin
def reject_kyc(request, kyc_id):
    if request.method == 'POST':
        kyc = get_object_or_404(KYC, id=kyc_id)
        kyc.approval_status = 'Rejected'
        kyc.remarks = request.POST.get('remarks', '').strip() or None
        kyc.save()
        messages.success(request, f'KYC for {kyc.user.get_full_name()} rejected.')
    return redirect('admin_kyc_detail', kyc_id=kyc_id)


# ─── User KYC Views ───────────────────────────────────────────────────────────

@login_required_user
def user_kyc_submit(request):
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    # Get existing KYC if any
    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        kyc = None

    if request.method == 'POST':
        pan_number     = request.POST.get('pan_number', '').strip().upper()
        aadhaar_number = request.POST.get('aadhaar_number', '').strip()
        pan_image      = request.FILES.get('pan_image')
        aadh_front     = request.FILES.get('aadhaar_front_image')
        aadh_back      = request.FILES.get('aadhaar_back_image')
        passbook_image = request.FILES.get('passbook_image')

        # Validate all uploaded images
        errors = []
        for label, file in [
            ('PAN Card', pan_image),
            ('Aadhaar Front', aadh_front),
            ('Aadhaar Back', aadh_back),
            ('Passbook/Cheque', passbook_image),
        ]:
            if file:
                err = validate_kyc_image(file)
                if err:
                    errors.append(f'{label}: {err}')

        if not kyc:
            # New submission — all 4 images required
            if not pan_image:
                errors.append('PAN Card image is required.')
            if not aadh_front:
                errors.append('Aadhaar Front image is required.')
            if not aadh_back:
                errors.append('Aadhaar Back image is required.')
            if not passbook_image:
                errors.append('Cancel Cheque / Passbook image is required.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'user/kyc_submit.html', {'kyc': kyc})

        if kyc:
            # Update existing
            kyc.pan_number     = pan_number or kyc.pan_number
            kyc.aadhaar_number = aadhaar_number or kyc.aadhaar_number
            if pan_image:
                kyc.pan_image = pan_image
            if aadh_front:
                kyc.aadhaar_front_image = aadh_front
            if aadh_back:
                kyc.aadhaar_back_image = aadh_back
            if passbook_image:
                kyc.passbook_image = passbook_image
            kyc.approval_status = 'Pending'   # reset on re-submit
            kyc.remarks = None
            kyc.save()
            messages.success(request, 'KYC details updated and re-submitted for review.')
        else:
            KYC.objects.create(
                user                = user,
                pan_number          = pan_number,
                aadhaar_number      = aadhaar_number,
                pan_image           = pan_image,
                aadhaar_front_image = aadh_front,
                aadhaar_back_image  = aadh_back,
                passbook_image      = passbook_image,
            )
            messages.success(request, 'KYC submitted successfully! Admin will review it shortly.')
        return redirect('user_kyc_detail')

    return render(request, 'user/kyc_submit.html', {'kyc': kyc})


@login_required_user
def user_kyc_detail(request):
    """Read-only view of the user's KYC submission."""
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        messages.info(request, 'You have not submitted KYC yet. Please fill the form below.')
        return redirect('user_kyc_submit')
    return render(request, 'user/kyc_detail.html', {'kyc': kyc})
