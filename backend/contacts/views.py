import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.email_utils import (
    send_contact_notification,
)

from .serializers import (
    ContactRequestSerializer,
)


logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_contact_request(request):

    serializer = ContactRequestSerializer(
        data=request.data
    )


    if serializer.is_valid():

        # Save to database first
        contact = serializer.save()

        email_sent = True


        try:

            send_contact_notification(
                contact
            )

        except Exception:

            email_sent = False

            logger.exception(
                'Contact notification email failed '
                'for contact ID %s',
                contact.id
            )


        return Response(
            {
                'success': True,
                'message':
                    'Your message has been received.',
                'email_sent': email_sent,
            },
            status=status.HTTP_201_CREATED
        )


    return Response(
        {
            'success': False,
            'errors': serializer.errors,
        },
        status=status.HTTP_400_BAD_REQUEST
    )