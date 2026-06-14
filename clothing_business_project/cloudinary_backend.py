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

        result = cloudinary.uploader.upload(
            content.read() if hasattr(content, 'read') else content,
            folder=folder,
            public_id=public_id_no_ext,
            resource_type='auto',
            overwrite=False,
            unique_filename=True,
        )
        # Store as "folder/public_id.format" so url() can reconstruct the Cloudinary URL
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
        return cloudinary.CloudinaryImage(public_id).url

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
