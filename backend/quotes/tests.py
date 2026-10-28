from io import BytesIO
from PIL import Image
from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import QuoteRequest


def photo_bytes():
    output = BytesIO()
    Image.new('RGB', (4, 4), 'white').save(output, format='JPEG')
    return output.getvalue()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    FILE_UPLOAD_MAX_MEMORY_SIZE=10 * 1024 * 1024,
    STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}},
)
class QuoteAttachmentEmailTests(TestCase):
    def submit(self, content=None):
        return self.client.post('/api/quote/', {
            'first_name': 'Test', 'last_name': 'Customer',
            'email': 'customer@example.com', 'phone': '123456',
            'service': 'residential_move', 'consent_accepted': True,
            'pickup_city': 'Koblenz', 'pickup_postal_code': '56068', 'pickup_floor': '0',
            'destination_city': 'Neuwied', 'destination_postal_code': '56564', 'destination_floor': '2',
            'files': [SimpleUploadedFile('photo.jpg', content or photo_bytes(), content_type='image/jpeg')],
        })

    def test_photo_sent_only_to_owner_and_customer_acknowledged(self):
        # Exercise a photo of the same size as the reported submission.
        content = photo_bytes() + b'\0' * 4_816_000
        response = self.submit(content)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['owner_email_sent'])
        self.assertTrue(response.data['customer_email_sent'])
        self.assertEqual(QuoteRequest.objects.get().attachments.count(), 1)
        self.assertEqual(len(mail.outbox), 2)
        owner, customer = mail.outbox
        self.assertEqual(owner.to, [settings.NOVARI_NOTIFICATION_EMAIL])
        self.assertEqual(len(owner.attachments), 1)
        name, body, mime = owner.attachments[0]
        self.assertEqual(name, 'photo.jpg')
        self.assertEqual(body, content)
        self.assertEqual(mime, 'image/jpeg')
        self.assertGreater(len(owner.message().as_bytes()), len(content))
        self.assertEqual(customer.to, ['customer@example.com'])
        self.assertEqual(customer.attachments, [])

    @patch('quotes.views.send_quote_notification', side_effect=TimeoutError('SMTP upload timed out'))
    def test_owner_timeout_preserves_quote_and_customer_acknowledgement(self, _send):
        with self.assertLogs('quotes.views', level='ERROR'):
            response = self.submit()
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data['owner_email_sent'])
        self.assertTrue(response.data['customer_email_sent'])
        self.assertEqual(QuoteRequest.objects.get().attachments.count(), 1)
        self.assertEqual(mail.outbox[0].to, ['customer@example.com'])


class QuoteLocationValidationTests(TestCase):
    def test_each_location_field_is_required_and_nonblank(self):
        from .serializers import QuoteRequestSerializer
        fields = ['pickup_city', 'pickup_postal_code', 'pickup_floor',
                  'destination_city', 'destination_postal_code', 'destination_floor']
        valid = dict(first_name='Test', last_name='Customer', email='test@example.com',
                     phone='123456', service='residential_move', consent_accepted=True,
                     pickup_city='Koblenz', pickup_postal_code='01234', pickup_floor='0',
                     destination_city='Neuwied', destination_postal_code='56564', destination_floor='EG')
        serializer = QuoteRequestSerializer(data=valid)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['pickup_postal_code'], '01234')
        self.assertEqual(serializer.validated_data['pickup_floor'], '0')
        for field in fields:
            for value in [None, '', '   ']:
                with self.subTest(field=field, value=value):
                    data = valid.copy()
                    if value is None:
                        data.pop(field)
                    else:
                        data[field] = value
                    serializer = QuoteRequestSerializer(data=data)
                    self.assertFalse(serializer.is_valid())
                    self.assertIn(field, serializer.errors)


class UploadValidationTests(TestCase):
    def test_rejects_disguised_or_corrupt_images_and_resets_stream(self):
        from .serializers import QuoteRequestSerializer
        for mime, content in [('image/jpeg', b'<script>bad</script>'),
                              ('image/png', photo_bytes()), ('video/mp4', b'not a video')]:
            upload = SimpleUploadedFile('file', content, content_type=mime)
            with self.subTest(mime=mime):
                with self.assertRaises(Exception) as error:
                    QuoteRequestSerializer().validate_files([upload])
                from rest_framework.exceptions import ValidationError
                self.assertIsInstance(error.exception, ValidationError)
                self.assertEqual(upload.tell(), 0)

    def test_count_and_aggregate_size_limits(self):
        from .serializers import QuoteRequestSerializer
        from rest_framework.exceptions import ValidationError
        files = [SimpleUploadedFile('photo.jpg', photo_bytes(), content_type='image/jpeg') for _ in range(7)]
        with self.assertRaises(ValidationError):
            QuoteRequestSerializer().validate_files(files)
        files[0].size = 14 * 1024 * 1024
        files[1].size = 14 * 1024 * 1024
        with self.assertRaises(ValidationError):
            QuoteRequestSerializer().validate_files(files[:2])

    def test_valid_photo_is_readable_after_validation(self):
        from .serializers import QuoteRequestSerializer
        upload = SimpleUploadedFile('photo.jpg', photo_bytes(), content_type='image/jpeg')
        self.assertEqual(QuoteRequestSerializer().validate_files([upload]), [upload])
        self.assertEqual(upload.read(), photo_bytes())

    def test_quote_requires_explicit_consent(self):
        from .serializers import QuoteRequestSerializer
        for value in [None, False]:
            data = {} if value is None else {'consent_accepted': value}
            serializer = QuoteRequestSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn('consent_accepted', serializer.errors)


@override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'}})
class PrivateAttachmentTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        from .models import QuoteAttachment
        self.staff = get_user_model().objects.create_user('staff', is_staff=True)
        self.other = get_user_model().objects.create_user('customer')
        quote = QuoteRequest.objects.create(first_name='Test', last_name='User',
                                            email='test@example.com', phone='123', service='residential_move')
        self.file = QuoteAttachment.objects.create(quote=quote,
            file=SimpleUploadedFile('private.jpg', photo_bytes(), content_type='image/jpeg'),
            original_name='private.jpg', content_type='image/jpeg', file_size=len(photo_bytes()))
        self.url = f'/admin/quote-files/{self.file.pk}/'

    def test_anonymous_and_nonstaff_cannot_download(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_staff_without_quote_permissions_cannot_download(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_authorized_staff_can_download_with_private_headers(self):
        from django.contrib.auth.models import Permission
        self.staff.user_permissions.add(Permission.objects.get(codename='view_quoterequest'))
        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b''.join(response.streaming_content), photo_bytes())
        self.assertEqual(response['Cache-Control'], 'private, no-store')
        self.assertIn('attachment;', response['Content-Disposition'])
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
        response.close()

    def test_public_media_url_is_not_served_even_in_development(self):
        with override_settings(DEBUG=True):
            self.assertEqual(self.client.get('/media/' + self.file.file.name).status_code, 404)
