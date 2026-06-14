import os
from django.http import FileResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import login_required_admin, paginate_queryset
from mainapp.models import CompanyDocument


TYPE_CHOICES = ['Policy', 'Certificate', 'Brochure', 'Manual', 'Legal', 'Other']


def _validate_pdf(file):
    if not file:
        return 'PDF file is required.'
    ext = os.path.splitext(file.name)[1].lower()
    if ext != '.pdf':
        return 'Only PDF files are allowed.'
    if file.size > 10 * 1024 * 1024:
        return 'File size must not exceed 10 MB.'
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
        doc_file = request.FILES.get('document_file')

        if not name or not doc_file:
            messages.error(request, 'Document name and PDF file are required.')
            return render(request, 'admin/documents/add_document.html', {'type_choices': TYPE_CHOICES})

        error = _validate_pdf(doc_file)
        if error:
            messages.error(request, error)
            return render(request, 'admin/documents/add_document.html', {'type_choices': TYPE_CHOICES})

        CompanyDocument.objects.create(
            document_name=name, document_type=doc_type if doc_type in TYPE_CHOICES else 'Other',
            description=desc or None, document_file=doc_file,
        )
        messages.success(request, f'Document "{name}" uploaded successfully.')
        return redirect('admin_documents')

    return render(request, 'admin/documents/add_document.html', {'type_choices': TYPE_CHOICES})


@login_required_admin
def edit_document(request, doc_id):
    doc = get_object_or_404(CompanyDocument, id=doc_id)
    if request.method == 'POST':
        name     = request.POST.get('document_name', '').strip()
        doc_type = request.POST.get('document_type', 'Other')
        desc     = request.POST.get('description', '').strip()
        doc_file = request.FILES.get('document_file')

        if not name:
            messages.error(request, 'Document name is required.')
            return render(request, 'admin/documents/edit_document.html', {
                'document': doc,
                'type_choices': TYPE_CHOICES,
            })

        if doc_file:
            error = _validate_pdf(doc_file)
            if error:
                messages.error(request, error)
                return render(request, 'admin/documents/edit_document.html', {
                    'document': doc,
                    'type_choices': TYPE_CHOICES,
                })
            doc.document_file = doc_file

        doc.document_name = name
        doc.document_type = doc_type if doc_type in TYPE_CHOICES else 'Other'
        doc.description = desc or None
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


def company_documents(request):
    docs = CompanyDocument.objects.all()
    selected_id = request.GET.get('doc')
    selected_doc = None
    if selected_id:
        selected_doc = docs.filter(id=selected_id).first()
    if not selected_doc:
        selected_doc = docs.first()
    return render(request, 'user/company_documents.html', {
        'documents': docs,
        'selected_doc': selected_doc,
    })


def document_download(request, doc_id):
    doc = get_object_or_404(CompanyDocument, id=doc_id)
    storage = doc.document_file.storage

    if hasattr(storage, 'download_url'):
        url = storage.download_url(doc.document_file.name)
        if url:
            return HttpResponseRedirect(url)

    try:
        file_path = doc.document_file.path
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        response = FileResponse(
            doc.document_file.open('rb'),
            as_attachment=True,
            filename=os.path.basename(doc.document_file.name),
            content_type='application/pdf',
        )
        return response
    except (AttributeError, NotImplementedError, FileNotFoundError):
        if doc.document_file.url:
            return HttpResponseRedirect(doc.document_file.url)
        raise Http404('Document file is not available.')
