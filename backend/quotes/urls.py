from django.urls import path

from .views import create_quote_request


urlpatterns = [
    path(
        '',
        create_quote_request,
        name='create-quote-request'
    ),
]
