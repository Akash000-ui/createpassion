"""
Management command to upload all existing local media files to Cloudinary
and update the database image fields to point to the Cloudinary URLs.

Usage (run in Render Shell after setting CLOUDINARY_URL env var):
    python manage.py upload_media_to_cloudinary
"""
import os
import cloudinary
import cloudinary.uploader
from django.core.management.base import BaseCommand
from django.conf import settings
from mainapp.models import UserProfile, Category, Product


class Command(BaseCommand):
    help = 'Upload existing local media files to Cloudinary and update DB paths'

    def handle(self, *args, **options):
        cfg = getattr(settings, 'CLOUDINARY_STORAGE', None)
        if not cfg:
            self.stdout.write(self.style.ERROR(
                'CLOUDINARY_URL env var is not set or invalid. Aborting.'
            ))
            return

        cloudinary.config(
            cloud_name=cfg['CLOUD_NAME'],
            api_key=cfg['API_KEY'],
            api_secret=cfg['API_SECRET'],
        )

        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if not media_root:
            self.stdout.write(self.style.ERROR('MEDIA_ROOT not set (running in cloud mode?). Aborting.'))
            return

        total = 0
        skipped = 0

        def upload_field(obj, field_name, folder):
            nonlocal total, skipped
            field = getattr(obj, field_name)
            if not field or not field.name:
                return
            old_name = field.name
            # Skip if already a Cloudinary path (contains 'res.cloudinary.com' or no extension path)
            if old_name.startswith('http') or '/' not in old_name and '.' not in old_name:
                skipped += 1
                return
            local_path = os.path.join(str(media_root), old_name)
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f'  File not found locally: {local_path}'))
                skipped += 1
                return
            try:
                result = cloudinary.uploader.upload(
                    local_path,
                    folder=folder,
                    use_filename=True,
                    unique_filename=False,
                    overwrite=True,
                )
                new_path = result['public_id'] + '.' + result['format']
                setattr(obj, field_name, new_path)
                obj.save(update_fields=[field_name])
                self.stdout.write(f'  ✓ {old_name}  →  {new_path}')
                total += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed {old_name}: {e}'))
                skipped += 1

        self.stdout.write('── UserProfile profile pics ─────────────────────')
        for user in UserProfile.objects.exclude(profile_pic='').exclude(profile_pic__isnull=True):
            upload_field(user, 'profile_pic', 'profile_pics')

        self.stdout.write('── Category images ──────────────────────────────')
        for cat in Category.objects.exclude(image='').exclude(image__isnull=True):
            upload_field(cat, 'image', 'category_images')

        self.stdout.write('── Product images ───────────────────────────────')
        for prod in Product.objects.exclude(image='').exclude(image__isnull=True):
            upload_field(prod, 'image', 'product_images')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done. Uploaded: {total}  |  Skipped/not found: {skipped}'
        ))
