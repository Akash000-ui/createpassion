from django.db import models
from .user_models import UserProfile


class Event(models.Model):
    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    event_name      = models.CharField(max_length=255)
    event_image     = models.ImageField(upload_to='event_images/', null=True, blank=True)
    description     = models.TextField(null=True, blank=True)
    event_date      = models.DateField()
    event_fee       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    venue           = models.CharField(max_length=500, null=True, blank=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def is_free(self):
        return self.event_fee == 0

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = 'events'
        ordering = ['-event_date']


class EventRegistration(models.Model):
    APPROVAL_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user                = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='event_registrations')
    event               = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    utr_number          = models.CharField(max_length=100, null=True, blank=True)
    payment_image       = models.ImageField(upload_to='event_payments/', null=True, blank=True)
    approval_status     = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='Pending')
    remarks             = models.TextField(null=True, blank=True)
    registration_date   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.event.event_name} [{self.approval_status}]"

    class Meta:
        db_table = 'event_registrations'
        unique_together = ('user', 'event')
        ordering = ['-registration_date']
