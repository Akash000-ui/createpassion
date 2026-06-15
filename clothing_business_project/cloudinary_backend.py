"""Cloudinary storage backend for application image uploads."""

import io
import os
import urllib.request

import cloudinary.uploader
import cloudinary.utils
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryMediaStorage(Storage):

    def _save(self, name, content):
        folder = os.path.dirname(name).replace('\\', '/')
        basename = os.path.basename(name)
        public_name = os.path.splitext(basename)[0]
        public_id = f'{folder}/{public_name}' if folder else public_name

        result = cloudinary.uploader.upload(
            content.read() if hasattr(content, 'read') else content,
            public_id=public_id,
            resource_type='image',
            overwrite=True,
            unique_filename=False,
            invalidate=True,
        )

        stored = result['public_id']
        file_format = result.get('format', '')
        return f'{stored}.{file_format}' if file_format else stored

    def exists(self, name):
        return False

    def url(self, name):
        if not name:
            return ''
        if name.startswith(('http://', 'https://')):
            return name

        public_id = os.path.splitext(name)[0].replace('\\', '/')
        url, _ = cloudinary.utils.cloudinary_url(
            public_id,
            resource_type='image',
            secure=True,
        )
        return url

    def _open(self, name, mode='rb'):
        data = urllib.request.urlopen(self.url(name)).read()
        return io.BytesIO(data)

    def delete(self, name):
        try:
            public_id = os.path.splitext(name)[0].replace('\\', '/')
            cloudinary.uploader.destroy(public_id, resource_type='image')
        except Exception:
            pass

    def size(self, name):
        return 0

    def get_available_name(self, name, max_length=None):
        return name
