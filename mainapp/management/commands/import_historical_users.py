import json
import os
from datetime import date, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_date, parse_datetime

from mainapp.models import UserProfile, WalletBalance


class Command(BaseCommand):
    help = 'Import historical UserProfile records from data.json without overwriting live users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            default='data.json',
            help='Fixture path (default: data.json)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate and report changes without writing to the database',
        )

    def _find_existing_user(self, fields):
        member_id = fields.get('member_id')
        email = fields.get('email')
        mobile = fields.get('mobile')

        if member_id:
            user = UserProfile.objects.filter(member_id=member_id).first()
            if user:
                return user
        if email:
            user = UserProfile.objects.filter(email__iexact=email).first()
            if user:
                return user
        if mobile:
            return UserProfile.objects.filter(mobile=mobile).first()
        return None

    def _parse_date(self, value):
        if isinstance(value, date):
            return value
        return parse_date(value) if value else None

    def _parse_datetime(self, value):
        if isinstance(value, datetime):
            return value
        return parse_datetime(value) if value else None

    @transaction.atomic
    def handle(self, *args, **options):
        filepath = options['file']
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)
        if not os.path.exists(filepath):
            raise CommandError(f'Fixture not found: {filepath}')

        with open(filepath, 'r', encoding='utf-8') as fixture_file:
            fixture = json.load(fixture_file)

        records = [
            record for record in fixture
            if record.get('model') == 'mainapp.userprofile'
        ]
        if not records:
            raise CommandError('No mainapp.userprofile records found in the fixture.')

        dry_run = options['dry_run']
        old_pk_to_user = {}
        created_old_pks = set()
        created = 0
        existing = 0
        linked = 0
        missing_parents = 0

        self.stdout.write(f'Historical users found: {len(records)}')

        for record in records:
            old_pk = record['pk']
            fields = record['fields']
            user = self._find_existing_user(fields)

            if user:
                WalletBalance.objects.get_or_create(user=user, defaults={'balance': 0})
                existing += 1
                old_pk_to_user[old_pk] = user
                continue

            user = UserProfile.objects.create(
                member_id=fields.get('member_id'),
                rank=fields.get('rank'),
                first_name=fields.get('first_name') or '',
                last_name=fields.get('last_name') or '',
                email=fields.get('email'),
                mobile=fields.get('mobile'),
                password=fields.get('password') or '',
                dob=self._parse_date(fields.get('dob')),
                gender=fields.get('gender'),
                marital_status=fields.get('marital_status'),
                address=fields.get('address'),
                city=fields.get('city'),
                state=fields.get('state'),
                country=fields.get('country') or 'India',
                pincode=fields.get('pincode'),
                profile_pic=fields.get('profile_pic') or None,
                income=Decimal(str(fields.get('income') or '0')),
                is_active=fields.get('is_active', True),
                is_admin=fields.get('is_admin', False),
            )

            historical_values = {}
            joining_date = self._parse_date(fields.get('joining_date'))
            created_at = self._parse_datetime(fields.get('created_at'))
            updated_at = self._parse_datetime(fields.get('updated_at'))
            if joining_date:
                historical_values['joining_date'] = joining_date
            if created_at:
                historical_values['created_at'] = created_at
            if updated_at:
                historical_values['updated_at'] = updated_at
            if historical_values:
                UserProfile.objects.filter(pk=user.pk).update(**historical_values)

            WalletBalance.objects.get_or_create(user=user, defaults={'balance': 0})
            old_pk_to_user[old_pk] = user
            created_old_pks.add(old_pk)
            created += 1

        for record in records:
            if record['pk'] not in created_old_pks:
                continue
            parent_old_pk = record['fields'].get('referred_by')
            if not parent_old_pk:
                continue

            user = old_pk_to_user.get(record['pk'])
            parent = old_pk_to_user.get(parent_old_pk)
            if not user or not parent:
                missing_parents += 1
                continue
            if user.referred_by_id != parent.pk:
                user.referred_by = parent
                user.save(update_fields=['referred_by'])
                linked += 1

        if dry_run:
            transaction.set_rollback(True)

        mode = 'DRY RUN' if dry_run else 'IMPORT COMPLETE'
        self.stdout.write(self.style.SUCCESS(
            f'{mode}: {created} created, {existing} already existed, '
            f'{linked} referral links set, {missing_parents} parents missing.'
        ))
