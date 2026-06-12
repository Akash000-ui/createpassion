from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from mainapp.utils.common_utils import login_required_user, login_required_admin, paginate_queryset
from mainapp.models import Message, UserProfile


# ─── User Side ────────────────────────────────────────────────────────────────

@login_required_user
def user_inbox(request):
    """All messages received by this user (from admin)."""
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    inbox = Message.objects.filter(
        receiver=user,
        is_admin_sender=True,
        parent__isnull=True,
    )
    page_obj = paginate_queryset(request, inbox, per_page=15)
    unread_count = inbox.filter(status='Unread').count()
    return render(request, 'user/messages/inbox.html', {
        'page_obj': page_obj,
        'unread_count': unread_count,
    })


@login_required_user
def user_sent(request):
    """Messages sent by this user to admin."""
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    sent = Message.objects.filter(
        sender=user,
        is_admin_receiver=True,
        parent__isnull=True,
    )
    page_obj = paginate_queryset(request, sent, per_page=15)
    return render(request, 'user/messages/sent.html', {'page_obj': page_obj})


@login_required_user
def user_compose(request):
    """User sends a new message to admin."""
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('message', '').strip()
        if not subject or not body:
            django_messages.error(request, 'Subject and message are required.')
            return redirect('user_compose')

        user = get_object_or_404(UserProfile, id=request.session['user_id'])
        Message.objects.create(
            sender=user,
            receiver=None,
            is_admin_sender=False,
            is_admin_receiver=True,
            subject=subject,
            message=body,
        )
        django_messages.success(request, 'Message sent to admin successfully.')
        return redirect('user_sent')

    return render(request, 'user/messages/compose.html')


@login_required_user
def user_message_thread(request, msg_id):
    """View a message thread and reply."""
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    # Allow viewing if user is sender or receiver
    msg = get_object_or_404(
        Message,
        id=msg_id,
        parent__isnull=True,
    )
    # Security: only the involved user can see this thread
    if msg.sender != user and msg.receiver != user:
        django_messages.error(request, 'Access denied.')
        return redirect('user_inbox')

    # Mark as read
    if msg.receiver == user and msg.status == 'Unread':
        msg.status = 'Read'
        msg.save(update_fields=['status'])

    # All replies in this thread
    replies = Message.objects.filter(parent=msg).order_by('created_at')

    if request.method == 'POST':
        body = request.POST.get('message', '').strip()
        if body:
            Message.objects.create(
                sender=user,
                receiver=None,
                is_admin_sender=False,
                is_admin_receiver=True,
                subject='Re: ' + msg.subject,
                message=body,
                parent=msg,
            )
            django_messages.success(request, 'Reply sent.')
        return redirect('user_message_thread', msg_id=msg_id)

    return render(request, 'user/messages/thread.html', {
        'msg': msg,
        'replies': replies,
    })


# ─── Admin Side ───────────────────────────────────────────────────────────────

@login_required_admin
def admin_inbox(request):
    """All messages received by admin (from users)."""
    inbox = Message.objects.filter(
        is_admin_receiver=True,
        parent__isnull=True,
    ).select_related('sender')
    page_obj = paginate_queryset(request, inbox, per_page=20)
    unread_count = Message.objects.filter(is_admin_receiver=True, status='Unread').count()
    return render(request, 'admin/messages/inbox.html', {
        'page_obj': page_obj,
        'unread_count': unread_count,
    })


@login_required_admin
def admin_sent(request):
    """Messages sent by admin to users."""
    sent = Message.objects.filter(
        is_admin_sender=True,
        parent__isnull=True,
    ).select_related('receiver')
    page_obj = paginate_queryset(request, sent, per_page=20)
    return render(request, 'admin/messages/sent.html', {'page_obj': page_obj})


@login_required_admin
def admin_compose(request):
    """Admin sends a message to one or more users identified by Member ID."""
    if request.method == 'POST':
        member_ids_raw = request.POST.get('member_ids', '').strip()
        subject = request.POST.get('subject', '').strip()
        body    = request.POST.get('message', '').strip()

        if not member_ids_raw or not subject or not body:
            django_messages.error(request, 'All fields are required.')
            return render(request, 'admin/messages/compose.html',
                          {'member_ids_raw': member_ids_raw, 'subject': subject, 'body': body})

        # Parse comma/space/newline-separated member IDs
        raw_ids = [x.strip() for x in member_ids_raw.replace('\n', ',').replace(' ', ',').split(',') if x.strip()]
        if not raw_ids:
            django_messages.error(request, 'Enter at least one Member ID.')
            return render(request, 'admin/messages/compose.html',
                          {'member_ids_raw': member_ids_raw, 'subject': subject, 'body': body})

        sent_to   = []
        not_found = []
        for mid in raw_ids:
            user = UserProfile.objects.filter(member_id__iexact=mid, is_admin=False).first()
            if not user:
                not_found.append(mid)
                continue
            Message.objects.create(
                sender=None,
                receiver=user,
                is_admin_sender=True,
                is_admin_receiver=False,
                subject=subject,
                message=body,
            )
            sent_to.append(user.get_full_name())

        if sent_to:
            django_messages.success(request, f'Message sent to {len(sent_to)} user(s): {", ".join(sent_to)}.')
        if not_found:
            django_messages.warning(request, f'Member ID(s) not found: {", ".join(not_found)}.')

        return redirect('admin_sent')

    return render(request, 'admin/messages/compose.html', {})


@login_required_admin
def admin_message_thread(request, msg_id):
    """Admin views a thread and can reply."""
    msg = get_object_or_404(Message, id=msg_id, parent__isnull=True)

    # Mark as read when admin opens it
    if msg.is_admin_receiver and msg.status == 'Unread':
        msg.status = 'Read'
        msg.save(update_fields=['status'])

    replies = Message.objects.filter(parent=msg).order_by('created_at')

    if request.method == 'POST':
        body = request.POST.get('message', '').strip()
        if body:
            # Reply goes back to whoever the original sender was
            receiver = msg.sender  # user who originally messaged admin
            Message.objects.create(
                sender=None,
                receiver=receiver,
                is_admin_sender=True,
                is_admin_receiver=False,
                subject='Re: ' + msg.subject,
                message=body,
                parent=msg,
            )
            django_messages.success(request, 'Reply sent to user.')
        return redirect('admin_message_thread', msg_id=msg_id)

    return render(request, 'admin/messages/thread.html', {
        'msg': msg,
        'replies': replies,
    })
