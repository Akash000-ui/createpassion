from django.db import models
from .user_models import UserProfile


class Message(models.Model):
    STATUS_CHOICES = [
        ('Unread', 'Unread'),
        ('Read', 'Read'),
    ]
    # sender/receiver can be a user or admin (admin stored as None with is_admin_sender=True)
    sender              = models.ForeignKey(
                            UserProfile, on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='sent_messages'
                        )
    receiver            = models.ForeignKey(
                            UserProfile, on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='received_messages'
                        )
    is_admin_sender     = models.BooleanField(default=False)  # True when admin sends
    is_admin_receiver   = models.BooleanField(default=False)  # True when sent to admin
    subject             = models.CharField(max_length=255)
    message             = models.TextField()
    parent              = models.ForeignKey(
                            'self', on_delete=models.SET_NULL,
                            null=True, blank=True, related_name='replies'
                        )  # for reply threading
    status              = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unread')
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender_name = 'Admin' if self.is_admin_sender else (self.sender.get_full_name() if self.sender else 'Unknown')
        return f"From {sender_name}: {self.subject}"

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
