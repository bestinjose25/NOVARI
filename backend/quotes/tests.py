from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import QuoteRequest


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
            'files': [SimpleUploadedFile('photo.jpg', content or b'photo data', content_type='image/jpeg')],
        })

    def test_photo_sent_only_to_owner_and_customer_acknowledged(self):
        # Exercise a photo of the same size as the reported submission.
        content = b'photo data' * 481632
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
