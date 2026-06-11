from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from mainapp.models import UserProfile, WalletBalance


class Command(BaseCommand):
    help = 'Create the initial admin user for VoidCloth'

    def handle(self, *args, **kwargs):
        email = 'admin@voidcloth.com'
        if UserProfile.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin user already exists: {email}'))
            return

        admin = UserProfile(
            first_name='Admin',
            last_name='VoidCloth',
            email=email,
            mobile='9000000000',
            password=make_password('Admin@123'),
            is_admin=True,
            is_active=True,
        )
        admin.save()
        WalletBalance.objects.create(user=admin, balance=0)

        self.stdout.write(self.style.SUCCESS('✅ Admin user created successfully!'))
        self.stdout.write(f'   Email   : {email}')
        self.stdout.write(f'   Password: Admin@123')
        self.stdout.write(self.style.WARNING('   ⚠ Please change the password after first login!'))
