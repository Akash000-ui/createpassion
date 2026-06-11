from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from mainapp.utils.common_utils import login_required_admin, login_required_user, paginate_queryset
from mainapp.utils.validators import validate_image_file
from mainapp.models import Event, EventRegistration


# ─── Admin Views ──────────────────────────────────────────────────────────────

@login_required_admin
def admin_events(request):
    status    = request.GET.get('status', '')
    events    = Event.objects.all()
    if status:
        events = events.filter(status=status)
    page_obj  = paginate_queryset(request, events, per_page=12)
    status_choices = ['Upcoming', 'Ongoing', 'Completed', 'Cancelled']
    return render(request, 'admin/events/admin_events.html', {
        'page_obj': page_obj,
        'selected_status': status,
        'status_choices': status_choices,
    })


@login_required_admin
def add_event(request):
    if request.method == 'POST':
        name        = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '').strip()
        event_date  = request.POST.get('event_date')
        event_fee   = request.POST.get('event_fee', '0')
        venue       = request.POST.get('venue', '').strip()
        status      = request.POST.get('status', 'Upcoming')
        image       = request.FILES.get('event_image')

        if not name or not event_date:
            messages.error(request, 'Event name and date are required.')
            return redirect('add_event')

        event = Event(
            event_name=name, description=description or None,
            event_date=event_date, event_fee=event_fee or 0,
            venue=venue or None, status=status,
        )
        if image:
            try:
                validate_image_file(image)
            except Exception as e:
                messages.error(request, str(e))
                return redirect('add_event')
            event.event_image = image
        event.save()
        messages.success(request, f'Event "{name}" created successfully.')
        return redirect('admin_events')

    return render(request, 'admin/events/add_event.html', {
        'status_choices': ['Upcoming', 'Ongoing', 'Completed', 'Cancelled']
    })


@login_required_admin
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        name        = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '').strip()
        event_date  = request.POST.get('event_date')
        event_fee   = request.POST.get('event_fee', '0')
        venue       = request.POST.get('venue', '').strip()
        status      = request.POST.get('status', 'Upcoming')
        image       = request.FILES.get('event_image')

        if not name or not event_date:
            messages.error(request, 'Event name and date are required.')
            return redirect('edit_event', event_id=event_id)

        event.event_name  = name
        event.description = description or None
        event.event_date  = event_date
        event.event_fee   = event_fee or 0
        event.venue       = venue or None
        event.status      = status
        if image:
            try:
                validate_image_file(image)
            except Exception as e:
                messages.error(request, str(e))
                return redirect('edit_event', event_id=event_id)
            event.event_image = image
        event.save()
        messages.success(request, f'Event "{name}" updated.')
        return redirect('admin_events')

    return render(request, 'admin/events/edit_event.html', {
        'event': event,
        'status_choices': ['Upcoming', 'Ongoing', 'Completed', 'Cancelled'],
    })


@login_required_admin
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        name = event.event_name
        event.delete()
        messages.success(request, f'Event "{name}" deleted.')
    return redirect('admin_events')


@login_required_admin
def event_registrations(request, event_id):
    event   = get_object_or_404(Event, id=event_id)
    status  = request.GET.get('status', '')
    regs    = EventRegistration.objects.filter(event=event).select_related('user')
    if status:
        regs = regs.filter(approval_status=status)
    page_obj = paginate_queryset(request, regs, per_page=15)
    return render(request, 'admin/events/event_registrations.html', {
        'event': event,
        'page_obj': page_obj,
        'selected_status': status,
    })


@login_required_admin
def approve_registration(request, reg_id):
    if request.method == 'POST':
        reg = get_object_or_404(EventRegistration, id=reg_id)
        reg.approval_status = 'Approved'
        reg.remarks = request.POST.get('remarks', '').strip() or None
        reg.save()
        messages.success(request, f'Registration for {reg.user.get_full_name()} approved.')
    return redirect('event_registrations', event_id=reg.event_id)


@login_required_admin
def reject_registration(request, reg_id):
    if request.method == 'POST':
        reg = get_object_or_404(EventRegistration, id=reg_id)
        reg.approval_status = 'Rejected'
        reg.remarks = request.POST.get('remarks', '').strip() or None
        reg.save()
        messages.success(request, f'Registration for {reg.user.get_full_name()} rejected.')
    return redirect('event_registrations', event_id=reg.event_id)


# ─── User Views ───────────────────────────────────────────────────────────────

def user_events(request):
    """Public events listing page — all upcoming/ongoing events."""
    status_filter = request.GET.get('status', '')
    events = Event.objects.exclude(status='Cancelled')
    if status_filter:
        events = events.filter(status=status_filter)
    page_obj = paginate_queryset(request, events, per_page=9)

    # Pass set of event IDs user is already registered for
    registered_ids = set()
    if request.session.get('user_id'):
        registered_ids = set(
            EventRegistration.objects.filter(
                user_id=request.session['user_id']
            ).values_list('event_id', flat=True)
        )

    return render(request, 'user/events/events_list.html', {
        'page_obj': page_obj,
        'registered_ids': registered_ids,
        'selected_status': status_filter,
        'status_choices': ['Upcoming', 'Ongoing', 'Completed'],
    })


def user_event_detail(request, event_id):
    """Single event detail page."""
    event = get_object_or_404(Event, id=event_id)
    registration = None
    if request.session.get('user_id'):
        registration = EventRegistration.objects.filter(
            user_id=request.session['user_id'], event=event
        ).first()
    return render(request, 'user/events/event_detail.html', {
        'event': event,
        'registration': registration,
    })


@login_required_user
def register_event(request, event_id):
    """User submits payment proof to register for an event."""
    from mainapp.models import UserProfile
    event = get_object_or_404(Event, id=event_id)
    user  = get_object_or_404(UserProfile, id=request.session['user_id'])

    # Already registered?
    existing = EventRegistration.objects.filter(user=user, event=event).first()
    if existing:
        messages.info(request, 'You have already registered for this event.')
        return redirect('user_event_detail', event_id=event_id)

    if event.status in ('Completed', 'Cancelled'):
        messages.error(request, 'This event is no longer accepting registrations.')
        return redirect('user_event_detail', event_id=event_id)

    if request.method == 'POST':
        utr_number    = request.POST.get('utr_number', '').strip()
        upi_id        = request.POST.get('upi_id', '').strip()
        payment_image = request.FILES.get('payment_image')

        errors = []
        if event.event_fee > 0:
            if not utr_number:
                errors.append('UTR / Transaction number is required.')
            if not payment_image:
                errors.append('Payment screenshot is required.')
        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'user/events/register_event.html', {
                'event': event
            })

        reg = EventRegistration(user=user, event=event)
        if event.event_fee > 0:
            reg.utr_number = utr_number
            if payment_image:
                try:
                    validate_image_file(payment_image)
                except Exception as e:
                    messages.error(request, str(e))
                    return render(request, 'user/events/register_event.html', {'event': event})
                reg.payment_image = payment_image
        # Store UPI id in remarks temporarily
        if upi_id:
            reg.remarks = f'UPI ID: {upi_id}'
        reg.save()

        messages.success(request, f'Registration submitted for "{event.event_name}". Admin will review and approve shortly.')
        return redirect('user_my_events')

    return render(request, 'user/events/register_event.html', {'event': event})


@login_required_user
def user_my_events(request):
    """User's registered events."""
    from mainapp.models import UserProfile
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    regs = EventRegistration.objects.filter(user=user).select_related('event')
    page_obj = paginate_queryset(request, regs, per_page=10)
    return render(request, 'user/events/my_events.html', {'page_obj': page_obj})


@login_required_user
def download_event_pass(request, reg_id):
    """Download event pass as a printable HTML page (only if approved)."""
    from mainapp.models import UserProfile
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    reg  = get_object_or_404(EventRegistration, id=reg_id, user=user)

    if reg.approval_status != 'Approved':
        messages.error(request, 'Event pass is only available after admin approval.')
        return redirect('user_my_events')

    return render(request, 'user/events/event_pass.html', {'reg': reg})



@login_required_admin
def admin_events(request):
    status    = request.GET.get('status', '')
    events    = Event.objects.all()
    if status:
        events = events.filter(status=status)
    page_obj  = paginate_queryset(request, events, per_page=12)
    status_choices = ['Upcoming', 'Ongoing', 'Completed', 'Cancelled']
    return render(request, 'admin/events/admin_events.html', {
        'page_obj': page_obj,
        'selected_status': status,
        'status_choices': status_choices,
    })


@login_required_admin
def add_event(request):
    if request.method == 'POST':
        name        = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '').strip()
        event_date  = request.POST.get('event_date')
        event_fee   = request.POST.get('event_fee', '0')
        venue       = request.POST.get('venue', '').strip()
        status      = request.POST.get('status', 'Upcoming')
        image       = request.FILES.get('event_image')

        if not name or not event_date:
            messages.error(request, 'Event name and date are required.')
            return redirect('add_event')

        event = Event(
            event_name=name, description=description or None,
            event_date=event_date, event_fee=event_fee or 0,
            venue=venue or None, status=status,
        )
        if image:
            try:
                validate_image_file(image)
            except Exception as e:
                messages.error(request, str(e))
                return redirect('add_event')
            event.event_image = image
        event.save()
        messages.success(request, f'Event "{name}" created successfully.')
        return redirect('admin_events')

    return render(request, 'admin/events/add_event.html', {
        'status_choices': ['Upcoming', 'Ongoing', 'Completed', 'Cancelled']
    })


@login_required_admin
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        name        = request.POST.get('event_name', '').strip()
        description = request.POST.get('description', '').strip()
        event_date  = request.POST.get('event_date')
        event_fee   = request.POST.get('event_fee', '0')
        venue       = request.POST.get('venue', '').strip()
        status      = request.POST.get('status', 'Upcoming')
        image       = request.FILES.get('event_image')

        if not name or not event_date:
            messages.error(request, 'Event name and date are required.')
            return redirect('edit_event', event_id=event_id)

        event.event_name  = name
        event.description = description or None
        event.event_date  = event_date
        event.event_fee   = event_fee or 0
        event.venue       = venue or None
        event.status      = status
        if image:
            try:
                validate_image_file(image)
            except Exception as e:
                messages.error(request, str(e))
                return redirect('edit_event', event_id=event_id)
            event.event_image = image
        event.save()
        messages.success(request, f'Event "{name}" updated.')
        return redirect('admin_events')

    return render(request, 'admin/events/edit_event.html', {
        'event': event,
        'status_choices': ['Upcoming', 'Ongoing', 'Completed', 'Cancelled'],
    })


@login_required_admin
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        name = event.event_name
        event.delete()
        messages.success(request, f'Event "{name}" deleted.')
    return redirect('admin_events')


@login_required_admin
def event_registrations(request, event_id):
    event   = get_object_or_404(Event, id=event_id)
    status  = request.GET.get('status', '')
    regs    = EventRegistration.objects.filter(event=event).select_related('user')
    if status:
        regs = regs.filter(approval_status=status)
    page_obj = paginate_queryset(request, regs, per_page=15)
    return render(request, 'admin/events/event_registrations.html', {
        'event': event,
        'page_obj': page_obj,
        'selected_status': status,
    })


@login_required_admin
def approve_registration(request, reg_id):
    if request.method == 'POST':
        reg = get_object_or_404(EventRegistration, id=reg_id)
        reg.approval_status = 'Approved'
        reg.remarks = request.POST.get('remarks', '').strip() or None
        reg.save()
        messages.success(request, f'Registration for {reg.user.get_full_name()} approved.')
    return redirect('event_registrations', event_id=reg.event_id)


@login_required_admin
def reject_registration(request, reg_id):
    if request.method == 'POST':
        reg = get_object_or_404(EventRegistration, id=reg_id)
        reg.approval_status = 'Rejected'
        reg.remarks = request.POST.get('remarks', '').strip() or None
        reg.save()
        messages.success(request, f'Registration for {reg.user.get_full_name()} rejected.')
    return redirect('event_registrations', event_id=reg.event_id)
