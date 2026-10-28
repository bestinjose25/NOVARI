from django.contrib import admin
from .downloads import attachment_download_link

from .models import (
    QuoteRequest,
    QuoteAttachment,
)


class QuoteAttachmentInline(
    admin.TabularInline
):

    model = QuoteAttachment

    extra = 0
    download = staticmethod(attachment_download_link)
    fields = ('original_name', 'download', 'content_type', 'file_size', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False

    readonly_fields = (
        'download',
        'original_name',
        'content_type',
        'file_size',
        'created_at',
    )


@admin.register(QuoteRequest)
class QuoteRequestAdmin(
    admin.ModelAdmin
):

    list_display = (
        'first_name',
        'last_name',
        'service',
        'phone',
        'preferred_date',
        'status',
        'created_at',
    )

    list_filter = (
        'service',
        'status',
        'created_at',
    )

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'pickup_city',
        'destination_city',
        'referral_source',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    inlines = [
        QuoteAttachmentInline
    ]


@admin.register(QuoteAttachment)
class QuoteAttachmentAdmin(
    admin.ModelAdmin
):
    download = staticmethod(attachment_download_link)
    fields = ('quote', 'original_name', 'download', 'content_type', 'file_size', 'created_at')
    readonly_fields = ('download', 'original_name', 'content_type', 'file_size', 'created_at')

    def has_add_permission(self, request):
        return False

    list_display = (
        'original_name',
        'quote',
        'content_type',
        'file_size',
        'created_at',
    )
