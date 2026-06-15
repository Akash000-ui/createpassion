from django.db import models
from urllib.parse import parse_qs, urlparse


class CompanyDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('Policy', 'Policy'),
        ('Certificate', 'Certificate'),
        ('Brochure', 'Brochure'),
        ('Manual', 'Manual'),
        ('Legal', 'Legal'),
        ('Other', 'Other'),
    ]

    document_name   = models.CharField(max_length=255)
    document_type   = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES, default='Other')
    google_drive_url = models.URLField(max_length=500)
    description     = models.TextField(null=True, blank=True)
    uploaded_date   = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def get_google_drive_file_id(self):
        parsed = urlparse(self.google_drive_url)
        parts = [part for part in parsed.path.split('/') if part]

        if 'd' in parts:
            index = parts.index('d')
            if index + 1 < len(parts):
                return parts[index + 1]

        query_id = parse_qs(parsed.query).get('id')
        return query_id[0] if query_id else ''

    def get_preview_url(self):
        file_id = self.get_google_drive_file_id()
        return f'https://drive.google.com/file/d/{file_id}/preview' if file_id else ''

    def get_download_url(self):
        file_id = self.get_google_drive_file_id()
        return f'https://drive.google.com/uc?export=download&id={file_id}' if file_id else ''

    def __str__(self):
        return self.document_name

    class Meta:
        db_table = 'company_documents'
        ordering = ['-uploaded_date']
