from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_GET

from .models import QuoteAttachment


@staff_member_required
@require_GET
def download_attachment(request, pk):
    if not (request.user.has_perm('quotes.view_quoteattachment') or
            request.user.has_perm('quotes.view_quoterequest')):
        raise PermissionDenied
    attachment = get_object_or_404(QuoteAttachment, pk=pk)
    try:
        stream = attachment.file.open('rb')
    except (OSError, ValueError):
        raise Http404('File unavailable')
    response = FileResponse(stream, as_attachment=True,
                            filename=attachment.original_name, content_type='application/octet-stream')
    response['Cache-Control'] = 'private, no-store'
    response['X-Content-Type-Options'] = 'nosniff'
    return response


def attachment_download_link(obj):
    if not obj.pk or not obj.file:
        return '-'
    return format_html('<a href="{}">Download file</a>', reverse('attachment-download', args=[obj.pk]))
