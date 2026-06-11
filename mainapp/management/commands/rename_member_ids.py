"""
Management command to rename all OL##### and RI##### member IDs to CP#####.

Usage:
    python manage.py rename_member_ids

The numeric part is preserved — OL20049 → CP20049, RI10023 → CP10023.
If two IDs would map to the same CP##### (e.g. OL20049 and RI20049 both → CP20049),
the second one gets a new unique suffix appended.
"""
import re
from django.core.management.base import BaseCommand
from mainapp.models import UserProfile


class Command(BaseCommand):
    help = 'Rename all OL##### / RI##### member IDs to CP#####'

    def handle(self, *args, **options):
        targets = UserProfile.objects.filter(
            member_id__iregex=r'^(OL|RI)\d+$'
        ).order_by('member_id')

        total    = targets.count()
        renamed  = 0
        skipped  = 0
        conflict = 0

        self.stdout.write(f'Found {total} member ID(s) to rename.')

        for user in targets:
            old_id = user.member_id
            m = re.match(r'^(?:OL|RI)(\d+)$', old_id)
            if not m:
                skipped += 1
                continue

            new_id = f'CP{m.group(1)}'

            # Handle conflict: if CP##### already taken, find next available
            if UserProfile.objects.filter(member_id=new_id).exclude(pk=user.pk).exists():
                # Find max CP number and go one beyond
                existing_cp = (
                    UserProfile.objects
                    .filter(member_id__startswith='CP')
                    .values_list('member_id', flat=True)
                )
                max_num = 10000
                for mid in existing_cp:
                    mm = re.match(r'^CP(\d+)$', mid or '')
                    if mm:
                        max_num = max(max_num, int(mm.group(1)))
                new_id = f'CP{max_num + 1}'
                conflict += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'  CONFLICT: {old_id} → reassigned to {new_id}'
                    )
                )

            user.member_id = new_id
            user.save(update_fields=['member_id'])
            renamed += 1
            self.stdout.write(f'  {old_id}  →  {new_id}')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done. Renamed: {renamed}  |  Conflicts resolved: {conflict}  |  Skipped: {skipped}'
        ))
