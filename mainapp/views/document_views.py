from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from mainapp.utils.common_utils import login_required_admin, paginate_queryset
from mainapp.utils.validators import validate_document_file
from mainapp.models import CompanyDocument


@login_required_admin
def admin_documents(request):
    doc_type = request.GET.get('type', '')
    docs     = CompanyDocument.objects.all()
    if doc_type:
        docs = docs.filter(document_type=doc_type)
    page_obj = paginate_queryset(request, docs, per_page=12)
    type_choices = ['Policy', 'Certificate', 'Brochure', 'Manual', 'Legal', 'Other']
    return render(request, 'admin/documents/admin_documents.html', {
        'page_obj': page_obj,
        'selected_type': doc_type,
        'type_choices': type_choices,
    })


@login_required_admin
def add_document(request):
    type_choices = ['Policy', 'Certificate', 'Brochure', 'Manual', 'Legal', 'Other']
    if request.method == 'POST':
        name     = request.POST.get('document_name', '').strip()
        doc_type = request.POST.get('document_type', 'Other')
        desc     = request.POST.get('description', '').strip()
        doc_file = request.FILES.get('document_file')

        if not name or not doc_file:
            messages.error(request, 'Document name and file are required.')
            return render(request, 'admin/documents/add_document.html', {'type_choices': type_choices})

        error = validate_document_file(doc_file)
        if error:
            messages.error(request, error)
            return render(request, 'admin/documents/add_document.html', {'type_choices': type_choices})

        CompanyDocument.objects.create(
            document_name=name, document_type=doc_type,
            description=desc or None, document_file=doc_file,
        )
        messages.success(request, f'Document "{name}" uploaded successfully.')
        return redirect('admin_documents')

    return render(request, 'admin/documents/add_document.html', {'type_choices': type_choices})


@login_required_admin
def delete_document(request, doc_id):
    if request.method == 'POST':
        doc = get_object_or_404(CompanyDocument, id=doc_id)
        name = doc.document_name
        doc.delete()
        messages.success(request, f'Document "{name}" deleted.')
    return redirect('admin_documents')
