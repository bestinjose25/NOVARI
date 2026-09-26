from django.urls import path
from .views import create_contact_request


urlpatterns = [
    path(
        '',
        create_contact_request,
        name='create-contact-request'
    ),
]