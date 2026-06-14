"""
Minimal Cloudinary media storage backend for Django 5.x.
Replaces django-cloudinary-storage (incompatible with Django 5.x).
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.utils
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tiff', '.svg'}

    def _resource_type(self, name):
        ext = os.path.splitext(str(name))[1].lower()
        return 'image' if ext in self.image_extensions else 'raw'

    def _public_id_for_save(self, name):
        folder = os.path.dirname(name).replace('\\', '/')
        basename = os.path.basename(name)
        resource_type = self._resource_type(name)
        public_name = os.path.splitext(basename)[0] if resource_type == 'image' else basename
        return f'{folder}/{public_name}' if folder else public_name

    def _public_id_for_url(self, name):
        clean_name = str(name).replace('\\', '/')
        if self._resource_type(clean_name) == 'image':
            return os.path.splitext(clean_name)[0]
        return clean_name

    def _save(self, name, content):
        full_public_id = self._public_id_for_save(name)
        resource_type = self._resource_type(name)

        result = cloudinary.uploader.upload(
            content.read() if hasattr(content, 'read') else content,
            public_id=full_public_id,
            resource_type=resource_type,
            overwrite=True,         # replace if same name exists
            unique_filename=False,  # do NOT append random suffix
            invalidate=True,        # bust CDN cache on overwrite
        )
        # Store as "public_id.format" — exactly what Cloudinary uses
        stored = result['public_id']
        fmt = result.get('format', '')
        if resource_type == 'image' and fmt:
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
        public_id = self._public_id_for_url(name)
        url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            resource_type=self._resource_type(name),
            secure=True,
        )
        return url

    def download_url(self, name):
        if not name:
            return ''
        if name.startswith('http://') or name.startswith('https://'):
            return name
        public_id = self._public_id_for_url(name)
        url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            resource_type=self._resource_type(name),
            secure=True,
            flags='attachment',
        )
        return url

    def _open(self, name, mode='rb'):
        import urllib.request
        import io
        data = urllib.request.urlopen(self.url(name)).read()
        return io.BytesIO(data)

    def delete(self, name):
        try:
            public_id = self._public_id_for_url(name)
            cloudinary.uploader.destroy(public_id, resource_type=self._resource_type(name))
        except Exception:
            pass

    def size(self, name):
        return 0

    def get_available_name(self, name, max_length=None):
        return name
