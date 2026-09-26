from django.contrib import admin
from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'phone',
        'created_at',
        'is_read',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'message',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
