from django.contrib import admin

from django.urls import (
    include,
    path,
)


from .views import health
from quotes.downloads import download_attachment


urlpatterns = [
    path('health/', health, name='health'),
    path('admin/quote-files/<int:pk>/', download_attachment, name='attachment-download'),

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/contact/',
        include('contacts.urls')
    ),

    path(
        'api/quote/',
        include('quotes.urls')
    ),
]


# Customer uploads are only accessible through permission-checked admin downloads.
