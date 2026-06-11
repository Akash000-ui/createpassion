"""
Management command: import_members
Usage: python manage.py import_members [--file final_members.xlsx]

Imports all members from the Excel sheet into UserProfile.
Pass 1: create all users.
Pass 2: link referred_by FK.
Skips rows with errors and continues.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
import openpyxl

from mainapp.models import UserProfile

# Excel rank → model rank code
RANK_MAP = {
    'FASHION CONSULTANT':        'FC',
    'FASHION ASSOCIATE':         'FA',
    'FASHION EXECUTIVE MANAGER': 'FEM',
    'CHIEF EXECUTIVE MANAGER':   'CEM',
    'RETAILER':                  'RT',
    'BUSINESS HEAD':             'BH',
    'BUSINESS AMBASSADOR':       'BA',
}

DEFAULT_PASSWORD = '12345678'


def split_name(full_name):
    """Split 'First Last...' into (first, last). If single word, last='.'"""
    parts = full_name.strip().split(None, 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], '.'


class Command(BaseCommand):
    help = 'Import members from final_members.xlsx into UserProfile'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', default='final_members.xlsx',
            help='Path to the Excel file (default: final_members.xlsx)'
        )

    def handle(self, *args, **options):
        filepath = options['file']
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)

        if not os.path.exists(filepath):
            self.stderr.write(self.style.ERROR(f'File not found: {filepath}'))
            return

        self.stdout.write(f'Loading: {filepath}')
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active

        rows = list(ws.iter_rows(min_row=2, values_only=True))
        self.stdout.write(f'Total rows: {len(rows)}')

        hashed_pw = make_password(DEFAULT_PASSWORD)

        # ── PASS 1: Create all users ──────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Pass 1: Creating users ---'))
        created = 0
        skipped = 0
        already_exists = 0

        for i, row in enumerate(rows, start=2):
            try:
                mid, name, email, rank_raw, ref_id, ref_name = row

                if not mid or not name:
                    self.stdout.write(f'  Row {i}: Skipped — missing ID or name')
                    skipped += 1
                    continue

                mid   = str(mid).strip()
                name  = str(name).strip()
                email = str(email).strip() if email else None
                rank  = RANK_MAP.get(str(rank_raw).strip().upper() if rank_raw else '', 'BH')

                # Skip if member_id already exists
                if UserProfile.objects.filter(member_id=mid).exists():
                    already_exists += 1
                    continue

                # Handle duplicate or missing email
                if email and UserProfile.objects.filter(email=email).exists():
                    # Make it unique by appending member_id
                    email = f'{mid}_{email}'

                first_name, last_name = split_name(name)

                UserProfile.objects.create(
                    member_id=mid,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    mobile=None,
                    password=hashed_pw,
                    rank=rank,
                    is_active=True,
                    is_admin=False,
                )
                created += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Row {i}: Error — {e}'))
                skipped += 1
                continue

        self.stdout.write(self.style.SUCCESS(
            f'Pass 1 done: {created} created, {already_exists} already existed, {skipped} skipped'
        ))

        # ── PASS 2: Link referred_by ──────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING('\n--- Pass 2: Linking referrals ---'))
        linked = 0
        link_skipped = 0

        for i, row in enumerate(rows, start=2):
            try:
                mid, name, email, rank_raw, ref_id, ref_name = row

                if not mid or not ref_id:
                    continue

                mid    = str(mid).strip()
                ref_id = str(ref_id).strip()

                try:
                    user   = UserProfile.objects.get(member_id=mid)
                    parent = UserProfile.objects.get(member_id=ref_id)
                except UserProfile.DoesNotExist:
                    link_skipped += 1
                    continue

                if user.referred_by_id != parent.id:
                    user.referred_by = parent
                    user.save(update_fields=['referred_by'])
                    linked += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  Row {i}: Link error — {e}'))
                link_skipped += 1
                continue

        self.stdout.write(self.style.SUCCESS(
            f'Pass 2 done: {linked} linked, {link_skipped} skipped'
        ))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Import complete. Total users in DB: {UserProfile.objects.filter(is_admin=False).count()}'
        ))
