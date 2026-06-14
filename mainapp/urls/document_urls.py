from django.urls import path
from mainapp.views import document_views

urlpatterns = [
    path('admin/documents',                        document_views.admin_documents, name='admin_documents'),
    path('admin/documents/add',                    document_views.add_document,    name='add_document'),
    path('admin/documents/<int:doc_id>/edit',      document_views.edit_document,   name='edit_document'),
    path('admin/documents/<int:doc_id>/delete',    document_views.delete_document, name='delete_document'),
    path('about-company',                          document_views.company_documents, name='company_documents'),
    path('company-documents/<int:doc_id>/view',     document_views.document_view, name='document_view'),
    path('company-documents/<int:doc_id>/download', document_views.document_download, name='document_download'),
]
