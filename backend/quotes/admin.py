from django.contrib import admin

from .models import (
    QuoteRequest,
    QuoteAttachment,
)


class QuoteAttachmentInline(
    admin.TabularInline
):

    model = QuoteAttachment

    extra = 0

    readonly_fields = (
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

    list_display = (
        'original_name',
        'quote',
        'content_type',
        'file_size',
        'created_at',
    )