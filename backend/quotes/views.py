import logging

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    parser_classes,
)
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework.response import Response

from config.email_utils import (
    send_quote_notification,
    send_quote_acknowledgement,
)

from .serializers import QuoteRequestSerializer


logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes([
    MultiPartParser,
    FormParser,
])
def create_quote_request(request):

    serializer = QuoteRequestSerializer(
        data=request.data
    )

    if serializer.is_valid():

        # Save quote + uploaded files first
        quote = serializer.save()

        owner_email_sent = True
        customer_email_sent = True

        # Email NOVARI owner
        try:
            send_quote_notification(quote)

        except Exception:
            owner_email_sent = False

            logger.exception(
                'NOVARI notification email failed '
                'for quote ID %s',
                quote.id
            )

        # Acknowledgement email to customer
        try:
            send_quote_acknowledgement(quote)

        except Exception:
            customer_email_sent = False

            logger.exception(
                'Customer acknowledgement email failed '
                'for quote ID %s',
                quote.id
            )

        return Response(
            {
                'success': True,
                'message':
                    'Your quote request has been received.',
                'quote_id':
                    quote.id,
                'owner_email_sent':
                    owner_email_sent,
                'customer_email_sent':
                    customer_email_sent,
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