from urllib.parse import urlparse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import login_required_admin, login_required_user, paginate_queryset
from mainapp.models import CompanyDocument, UserProfile


TYPE_CHOICES = ['Policy', 'Certificate', 'Brochure', 'Manual', 'Legal', 'Other']


def _validate_google_drive_url(url):
    if not url:
        return 'Google Drive link is required.'

    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc not in {'drive.google.com', 'www.drive.google.com'}:
        return 'Enter a valid Google Drive file link.'

    document = CompanyDocument(google_drive_url=url)
    if not document.get_google_drive_file_id():
        return 'The Google Drive file ID could not be found in this link.'

    return None


@login_required_admin
def admin_documents(request):
    doc_type = request.GET.get('type', '')
    docs     = CompanyDocument.objects.all()
    if doc_type:
        docs = docs.filter(document_type=doc_type)
    page_obj = paginate_queryset(request, docs, per_page=12)
    return render(request, 'admin/documents/admin_documents.html', {
        'page_obj': page_obj,
        'selected_type': doc_type,
        'type_choices': TYPE_CHOICES,
    })


@login_required_admin
def add_document(request):
    if request.method == 'POST':
        name     = request.POST.get('document_name', '').strip()
        doc_type = request.POST.get('document_type', 'Other')
        desc     = request.POST.get('description', '').strip()
        drive_url = request.POST.get('google_drive_url', '').strip()

        if not name or not drive_url:
            messages.error(request, 'Document name and Google Drive link are required.')
            return render(request, 'admin/documents/add_document.html', {'type_choices': TYPE_CHOICES})

        error = _validate_google_drive_url(drive_url)
        if error:
            messages.error(request, error)
            return render(request, 'admin/documents/add_document.html', {'type_choices': TYPE_CHOICES})

        CompanyDocument.objects.create(
            document_name=name, document_type=doc_type if doc_type in TYPE_CHOICES else 'Other',
            description=desc or None, google_drive_url=drive_url,
        )
        messages.success(request, f'Document "{name}" added successfully.')
        return redirect('admin_documents')

    return render(request, 'admin/documents/add_document.html', {'type_choices': TYPE_CHOICES})


@login_required_admin
def edit_document(request, doc_id):
    doc = get_object_or_404(CompanyDocument, id=doc_id)
    if request.method == 'POST':
        name     = request.POST.get('document_name', '').strip()
        doc_type = request.POST.get('document_type', 'Other')
        desc     = request.POST.get('description', '').strip()
        drive_url = request.POST.get('google_drive_url', '').strip()

        if not name or not drive_url:
            messages.error(request, 'Document name and Google Drive link are required.')
            return render(request, 'admin/documents/edit_document.html', {
                'document': doc,
                'type_choices': TYPE_CHOICES,
            })

        error = _validate_google_drive_url(drive_url)
        if error:
            messages.error(request, error)
            return render(request, 'admin/documents/edit_document.html', {
                'document': doc,
                'type_choices': TYPE_CHOICES,
            })

        doc.document_name = name
        doc.document_type = doc_type if doc_type in TYPE_CHOICES else 'Other'
        doc.description = desc or None
        doc.google_drive_url = drive_url
        doc.save()
        messages.success(request, f'Document "{name}" updated successfully.')
        return redirect('admin_documents')

    return render(request, 'admin/documents/edit_document.html', {
        'document': doc,
        'type_choices': TYPE_CHOICES,
    })


@login_required_admin
def delete_document(request, doc_id):
    if request.method == 'POST':
        doc = get_object_or_404(CompanyDocument, id=doc_id)
        name = doc.document_name
        doc.delete()
        messages.success(request, f'Document "{name}" deleted.')
    return redirect('admin_documents')


@login_required_user
def company_documents(request):
    user = get_object_or_404(UserProfile, id=request.session['user_id'])
    docs = CompanyDocument.objects.exclude(google_drive_url='')
    selected_id = request.GET.get('doc')
    selected_doc = None
    if selected_id:
        selected_doc = docs.filter(id=selected_id).first()
    if not selected_doc:
        selected_doc = docs.first()
    return render(request, 'user/company_documents.html', {
        'profile': user,
        'documents': docs,
        'selected_doc': selected_doc,
    })
