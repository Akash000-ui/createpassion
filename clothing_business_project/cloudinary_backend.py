"""
Minimal Cloudinary media storage backend for Django 5.x.
Replaces django-cloudinary-storage (incompatible with Django 5.x).
"""
import os
import cloudinary
import cloudinary.uploader
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):

    def _save(self, name, content):
        folder = os.path.dirname(name).replace('\\', '/')
        basename = os.path.basename(name)
        public_id_no_ext = os.path.splitext(basename)[0]
        # Build the full public_id including folder
        full_public_id = f'{folder}/{public_id_no_ext}' if folder else public_id_no_ext

        result = cloudinary.uploader.upload(
            content.read() if hasattr(content, 'read') else content,
            public_id=full_public_id,
            resource_type='auto',
            overwrite=True,         # replace if same name exists
            unique_filename=False,  # do NOT append random suffix
            invalidate=True,        # bust CDN cache on overwrite
        )
        # Store as "public_id.format" — exactly what Cloudinary uses
        stored = result['public_id']
        fmt = result.get('format', '')
        if fmt:
            stored = stored + '.' + fmt
        return stored

    def exists(self, name):
        # Let Cloudinary handle deduplication via unique_filename=True
        return False

    def url(self, name):
        if not name:
            return ''
        if name.startswith('http://') or name.startswith('https://'):
            return name
        # Strip extension to get Cloudinary public_id
        public_id = os.path.splitext(name)[0].replace('\\', '/')
        url, _ = cloudinary.utils.cloudinary_url(public_id, resource_type='image')
        return url

    def _open(self, name, mode='rb'):
        import urllib.request
        import io
        data = urllib.request.urlopen(self.url(name)).read()
        return io.BytesIO(data)

    def delete(self, name):
        try:
            public_id = os.path.splitext(name)[0].replace('\\', '/')
            cloudinary.uploader.destroy(public_id)
        except Exception:
            pass

    def size(self, name):
        return 0

    def get_available_name(self, name, max_length=None):
        return name
