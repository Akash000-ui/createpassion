from django.db import models
from .user_models import UserProfile


class WalletRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user                = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='wallet_requests')
    utr_number          = models.CharField(max_length=100)
    transaction_number  = models.CharField(max_length=100, null=True, blank=True)
    receipt_image       = models.ImageField(upload_to='wallet_receipts/')
    amount              = models.DecimalField(max_digits=12, decimal_places=2)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks             = models.TextField(null=True, blank=True)
    submitted_date      = models.DateTimeField(auto_now_add=True)
    approved_date       = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Wallet Request ₹{self.amount} by {self.user.get_full_name()} [{self.status}]"

    class Meta:
        db_table = 'wallet_requests'
        ordering = ['-submitted_date']


class WalletBalance(models.Model):
    """Tracks running wallet balance per user."""
    user            = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wallet')
    balance         = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Balance: ₹{self.balance}"

    class Meta:
        db_table = 'wallet_balances'
