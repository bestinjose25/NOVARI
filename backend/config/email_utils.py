from django.conf import settings

from django.core.mail import (
    EmailMessage,
    EmailMultiAlternatives,
)

from django.template.loader import (
    render_to_string,
)

from django.utils import timezone


# ======================================================
# GERMAN SERVICE NAMES
# ======================================================

GERMAN_SERVICE_NAMES = {
    'residential_move':
        'Privatumzug',

    'business_move':
        'Firmenumzug',

    'furniture_transport':
        'Möbeltransport',

    'furniture_assembly':
        'Möbelmontage / Demontage',

    'household_clearance':
        'Haushaltsauflösung',

    'carrying_assistance':
        'Tragehilfe',

    'handyman':
        'Kleinarbeiten / Handwerkerhilfe',

    'not_sure':
        'Noch nicht sicher',
}


def get_german_service_name(quote):
    """
    Convert the service value stored in the database
    into the German service name used in emails.
    """

    return GERMAN_SERVICE_NAMES.get(
        quote.service,
        quote.get_service_display()
    )


# ======================================================
# CONTACT NOTIFICATION TO NOVARI
# ======================================================

def send_contact_notification(contact):

    submitted_at = timezone.localtime(
        contact.created_at
    ).strftime(
        '%d.%m.%Y %H:%M'
    )


    subject = (
        f'Neue NOVARI Kontaktanfrage - '
        f'{contact.name}'
    )


    message = f"""
Eine neue Kontaktanfrage wurde über die NOVARI-Website gesendet.

KUNDE
================================

Name:
{contact.name}

E-Mail:
{contact.email}

Telefon:
{contact.phone or '-'}


NACHRICHT
================================

{contact.message}


ANFRAGEINFORMATIONEN
================================

Kontaktanfrage-ID:
{contact.id}

Eingereicht am:
{submitted_at}


Diese Anfrage wurde ebenfalls in der NOVARI-Datenbank gespeichert.
""".strip()


    email = EmailMessage(
        subject=subject,

        body=message,

        from_email=
            settings.DEFAULT_FROM_EMAIL,

        to=[
            settings.NOVARI_NOTIFICATION_EMAIL
        ],

        # Clicking Reply sends the response
        # directly to the customer
        reply_to=[
            contact.email
        ],
    )


    email.send(
        fail_silently=False
    )


# ======================================================
# QUOTE NOTIFICATION TO NOVARI OWNER
# ======================================================

def send_quote_notification(quote):

    # --------------------------------------------------
    # Date / time
    # --------------------------------------------------

    submitted_at = timezone.localtime(
        quote.created_at
    ).strftime(
        '%d.%m.%Y %H:%M'
    )


    preferred_date = (
        quote.preferred_date.strftime(
            '%d.%m.%Y'
        )
        if quote.preferred_date
        else '-'
    )


    # --------------------------------------------------
    # Elevator values in German
    # --------------------------------------------------

    pickup_elevator = (
        'Ja'
        if quote.pickup_elevator
        else 'Nein'
    )


    destination_elevator = (
        'Ja'
        if quote.destination_elevator
        else 'Nein'
    )


    # --------------------------------------------------
    # Number of uploaded files
    # --------------------------------------------------

    attachment_count = (
        quote.attachments.count()
    )


    # --------------------------------------------------
    # German service name
    # --------------------------------------------------

    service = get_german_service_name(
        quote
    )


    # --------------------------------------------------
    # Django Admin URL
    # --------------------------------------------------

    site_url = getattr(
        settings,
        'SITE_URL',
        'http://127.0.0.1:8001'
    )


    admin_url = (
        f'{site_url}'
        f'/admin/quotes/'
        f'quoterequest/'
        f'{quote.id}/change/'
    )


    # --------------------------------------------------
    # Data sent to HTML template
    # --------------------------------------------------

    context = {

        'quote':
            quote,

        'service':
            service,

        'submitted_at':
            submitted_at,

        'preferred_date':
            preferred_date,

        'pickup_elevator':
            pickup_elevator,

        'destination_elevator':
            destination_elevator,

        'attachment_count':
            attachment_count,

        'admin_url':
            admin_url,
    }


    # --------------------------------------------------
    # Render HTML email
    # --------------------------------------------------

    html_content = render_to_string(
        'emails/quote_notification.html',
        context
    )


    # --------------------------------------------------
    # Plain-text fallback
    # --------------------------------------------------

    text_content = f"""
NEUE NOVARI ANGEBOTSANFRAGE #{quote.id}

KUNDE
================================

Name:
{quote.first_name} {quote.last_name}

E-Mail:
{quote.email}

Telefon:
{quote.phone}

Dienstleistung:
{service}


ABHOLUNG
================================

Adresse:
{quote.pickup_address or '-'}

PLZ / Ort:
{quote.pickup_postal_code} {quote.pickup_city}

Etage:
{quote.pickup_floor or '-'}

Aufzug:
{pickup_elevator}


ZIEL
================================

Adresse:
{quote.destination_address or '-'}

PLZ / Ort:
{quote.destination_postal_code} {quote.destination_city}

Etage:
{quote.destination_floor or '-'}

Aufzug:
{destination_elevator}


UMZUGSDETAILS
================================

Wunschtermin:
{preferred_date}

Gegenstände:
{quote.items or '-'}

Zusätzliche Informationen:
{quote.notes or '-'}


DATEIEN
================================

Hochgeladene Dateien:
{attachment_count}


ANFRAGEINFORMATIONEN
================================

Anfrage-ID:
{quote.id}

Eingereicht am:
{submitted_at}
""".strip()


    # --------------------------------------------------
    # Subject
    # --------------------------------------------------

    subject = (
        f'Neue NOVARI Angebotsanfrage '
        f'#{quote.id} - {service}'
    )


    # --------------------------------------------------
    # Create email
    # --------------------------------------------------

    email = EmailMultiAlternatives(

        subject=subject,

        body=text_content,

        from_email=
            settings.DEFAULT_FROM_EMAIL,

        # Owner / NOVARI receives this email
        to=[
            settings.NOVARI_NOTIFICATION_EMAIL
        ],

        # Clicking Reply sends reply
        # directly to customer
        reply_to=[
            quote.email
        ],
    )


    # --------------------------------------------------
    # Add HTML version
    # --------------------------------------------------

    email.attach_alternative(
        html_content,
        'text/html'
    )


    # ==================================================
    # ATTACH CUSTOMER PHOTOS AND VIDEOS
    # ==================================================

    # Keep the combined raw attachment size reasonably
    # below common email-provider limits.
    MAX_TOTAL_ATTACHMENT_SIZE = (
        15 * 1024 * 1024
    )


    allowed_types = [
        'image/jpeg',
        'image/png',
        'image/webp',
        'video/mp4',
    ]


    total_size = 0


    for attachment in quote.attachments.all():

        print(
            'FOUND ATTACHMENT:',
            attachment.original_name,
            attachment.content_type,
            attachment.file_size
        )


        # ----------------------------------------------
        # Check file type
        # ----------------------------------------------

        if (
            attachment.content_type
            not in allowed_types
        ):

            print(
                'SKIPPED TYPE:',
                attachment.original_name
            )

            continue


        # ----------------------------------------------
        # Check combined size
        # ----------------------------------------------

        if (
            total_size
            + attachment.file_size
            > MAX_TOTAL_ATTACHMENT_SIZE
        ):

            print(
                'SKIPPED SIZE:',
                attachment.original_name
            )

            continue


        # ----------------------------------------------
        # Open saved file
        # ----------------------------------------------

        attachment.file.open(
            'rb'
        )


        try:

            file_content = (
                attachment.file.read()
            )


            # ------------------------------------------
            # Attach the actual file to email
            # ------------------------------------------

            email.attach(
                attachment.original_name,
                file_content,
                attachment.content_type
            )


            total_size += (
                attachment.file_size
            )


            print(
                'ATTACHED TO EMAIL:',
                attachment.original_name
            )


        finally:

            attachment.file.close()


    print(
        'FILES ATTACHED TO EMAIL:',
        len(email.attachments)
    )


    # ==================================================
    # SEND EMAIL
    # ==================================================

    # Important:
    # Sending happens AFTER all attachments have
    # been added.

    email.send(
        fail_silently=False
    )


# ======================================================
# CUSTOMER QUOTE ACKNOWLEDGEMENT
# ======================================================

def send_quote_acknowledgement(quote):

    # --------------------------------------------------
    # Preferred date
    # --------------------------------------------------

    preferred_date = (
        quote.preferred_date.strftime(
            '%d.%m.%Y'
        )
        if quote.preferred_date
        else '-'
    )


    # --------------------------------------------------
    # Uploaded file count
    # --------------------------------------------------

    attachment_count = (
        quote.attachments.count()
    )


    # --------------------------------------------------
    # German service name
    # --------------------------------------------------

    service = get_german_service_name(
        quote
    )


    # --------------------------------------------------
    # HTML template context
    # --------------------------------------------------

    context = {

        'quote':
            quote,

        'service':
            service,

        'preferred_date':
            preferred_date,

        'attachment_count':
            attachment_count,
    }


    # --------------------------------------------------
    # Render customer acknowledgement HTML
    # --------------------------------------------------

    html_content = render_to_string(
        'emails/quote_acknowledgement.html',
        context
    )


    # --------------------------------------------------
    # Plain-text fallback
    # --------------------------------------------------

    text_content = f"""
Hallo {quote.first_name},

vielen Dank für Ihre Anfrage bei NOVARI.

Wir haben Ihre Angebotsanfrage erfolgreich erhalten.

ANFRAGE-NR.
================================

#{quote.id}


DIENSTLEISTUNG
================================

{service}


WUNSCHTERMIN
================================

{preferred_date}


ABHOLORT
================================

{quote.pickup_postal_code} {quote.pickup_city}


ZIELORT
================================

{quote.destination_postal_code} {quote.destination_city}


Unsere Mitarbeiter werden Ihre Anfrage prüfen und sich schnellstmöglich mit Ihnen in Verbindung setzen.

Falls Sie weitere Informationen ergänzen möchten, können Sie einfach auf diese E-Mail antworten.

Viele Grüße

NOVARI GbR
Koblenz
""".strip()


    # --------------------------------------------------
    # Create acknowledgement email
    # --------------------------------------------------

    email = EmailMultiAlternatives(

        subject=(
            f'Ihre Anfrage bei NOVARI '
            f'#{quote.id} wurde erhalten'
        ),

        body=text_content,

        from_email=
            settings.DEFAULT_FROM_EMAIL,

        # Customer receives acknowledgement
        to=[
            quote.email
        ],

        # If customer clicks Reply,
        # the response goes to NOVARI
        reply_to=[
            settings.NOVARI_NOTIFICATION_EMAIL
        ],
    )


    # --------------------------------------------------
    # HTML version
    # --------------------------------------------------

    email.attach_alternative(
        html_content,
        'text/html'
    )


    # --------------------------------------------------
    # Send acknowledgement
    # --------------------------------------------------

    email.send(
        fail_silently=False
    )