from django.db import models
from .user_models import UserProfile


class BankDetails(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    ]
    APPROVAL_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user                    = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='bank_details')
    account_holder_name     = models.CharField(max_length=200)
    bank_name               = models.CharField(max_length=200)
    branch_name             = models.CharField(max_length=200, null=True, blank=True)
    account_number          = models.CharField(max_length=50)
    ifsc_code               = models.CharField(max_length=20)
    account_type            = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='Savings')
    approval_status         = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='Pending')
    remarks                 = models.TextField(null=True, blank=True)
    submitted_at            = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.bank_name} [{self.approval_status}]"

    class Meta:
        db_table = 'bank_details'
