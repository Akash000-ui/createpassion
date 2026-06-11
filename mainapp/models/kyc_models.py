from django.db import models
from .user_models import UserProfile


class KYC(models.Model):
    APPROVAL_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user                    = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='kyc')
    pan_number              = models.CharField(max_length=20, null=True, blank=True)
    aadhaar_number          = models.CharField(max_length=20, null=True, blank=True)
    pan_image               = models.ImageField(upload_to='kyc_documents/pan/', null=True, blank=True)
    aadhaar_front_image     = models.ImageField(upload_to='kyc_documents/aadhaar/', null=True, blank=True)
    aadhaar_back_image      = models.ImageField(upload_to='kyc_documents/aadhaar/', null=True, blank=True)
    passbook_image          = models.ImageField(upload_to='kyc_documents/passbook/', null=True, blank=True)
    approval_status         = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='Pending')
    remarks                 = models.TextField(null=True, blank=True)
    submitted_at            = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYC - {self.user.get_full_name()} [{self.approval_status}]"

    class Meta:
        db_table = 'kyc_details'
