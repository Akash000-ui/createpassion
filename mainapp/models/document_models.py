from django.db import models


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
    document_file   = models.FileField(upload_to='company_documents/')
    description     = models.TextField(null=True, blank=True)
    uploaded_date   = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def get_file_extension(self):
        name = self.document_file.name
        return name.split('.')[-1].upper() if '.' in name else 'FILE'

    def __str__(self):
        return self.document_name

    class Meta:
        db_table = 'company_documents'
        ordering = ['-uploaded_date']
