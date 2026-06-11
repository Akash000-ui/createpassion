from django.urls import path
from mainapp.views import document_views

urlpatterns = [
    path('admin/documents',                        document_views.admin_documents, name='admin_documents'),
    path('admin/documents/add',                    document_views.add_document,    name='add_document'),
    path('admin/documents/<int:doc_id>/delete',    document_views.delete_document, name='delete_document'),
]

