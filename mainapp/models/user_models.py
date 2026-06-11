from django.db import models
from django.contrib.auth.hashers import make_password


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    MARITAL_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]
    RANK_CHOICES = [
        ('FC',  'Fashion Consultant'),
        ('FA',  'Fashion Associate'),
        ('FEM', 'Fashion Executive Manager'),
        ('CEM', 'Chief Executive Manager'),
        ('BH',  'Business Head'),
        ('BA',  'Business Ambassador'),
        ('RT',  'Retailer'),
    ]

    # ── MLM / Network fields ──────────────────────────────────────────────────
    member_id   = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rank        = models.CharField(max_length=10, choices=RANK_CHOICES, null=True, blank=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='referrals'
    )

    # ── Core profile ──────────────────────────────────────────────────────────
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    email           = models.EmailField(unique=True, null=True, blank=True)
    mobile          = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password        = models.CharField(max_length=255)
    dob             = models.DateField(null=True, blank=True)
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status  = models.CharField(max_length=20, choices=MARITAL_CHOICES, null=True, blank=True)
    address         = models.TextField(null=True, blank=True)
    city            = models.CharField(max_length=100, null=True, blank=True)
    state           = models.CharField(max_length=100, null=True, blank=True)
    country         = models.CharField(max_length=100, default='India')
    pincode         = models.CharField(max_length=10, null=True, blank=True)
    profile_pic     = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    income          = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    joining_date    = models.DateField(auto_now_add=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return '/static/images/default_avatar.png'

    def get_commission_pct(self):
        return {'FC': 21, 'FA': 30, 'FEM': 39, 'CEM': 42, 'BH': 43, 'BA': 44, 'RT': 11}.get(self.rank)

    def get_rank_display_name(self):
        return dict(self.RANK_CHOICES).get(self.rank, 'Unknown')

    def __str__(self):
        return f"{self.get_full_name()} ({self.member_id or self.email})"

    class Meta:
        db_table = 'user_profiles'
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
