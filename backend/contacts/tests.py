from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings

from .models import ContactRequest


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ContactEmailTests(TestCase):
    def submit(self):
        return self.client.post('/api/contact/', {
            'name': 'Test Customer',
            'email': 'customer@example.com',
            'phone': '',
            'message': 'Hello <script>alert(1)</script>\nA second line.',
            'consent_accepted': True,
        })

    def test_owner_and_customer_receive_multipart_emails(self):
        response = self.submit()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['owner_email_sent'])
        self.assertTrue(response.data['customer_email_sent'])
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)
        owner, customer = mail.outbox
        self.assertEqual(owner.to, [settings.NOVARI_NOTIFICATION_EMAIL])
        self.assertEqual(owner.reply_to, ['customer@example.com'])
        self.assertEqual(customer.to, ['customer@example.com'])
        self.assertEqual(customer.reply_to, [settings.NOVARI_NOTIFICATION_EMAIL])
        for email in mail.outbox:
            self.assertIn('A second line.', email.body)
            html, content_type = email.alternatives[0]
            self.assertEqual(content_type, 'text/html')
            self.assertIn('NOVARI', html)
            self.assertIn('&lt;script&gt;', html)
            self.assertNotIn('<script>', html)

    @patch('contacts.views.send_contact_notification', side_effect=RuntimeError('SMTP unavailable'))
    def test_customer_email_still_attempted_after_owner_failure(self, _send):
        with self.assertLogs('contacts.views', level='ERROR'):
            response = self.submit()
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.data['email_sent'])
        self.assertTrue(response.data['customer_email_sent'])
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(mail.outbox[0].to, ['customer@example.com'])

    @patch('contacts.views.send_contact_acknowledgement', side_effect=RuntimeError('SMTP unavailable'))
    def test_owner_email_and_message_preserved_after_customer_failure(self, _send):
        with self.assertLogs('contacts.views', level='ERROR'):
            response = self.submit()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['email_sent'])
        self.assertFalse(response.data['customer_email_sent'])
        self.assertEqual(ContactRequest.objects.count(), 1)
        self.assertEqual(mail.outbox[0].to, [settings.NOVARI_NOTIFICATION_EMAIL])


class ContactConsentTests(TestCase):
    def test_missing_false_and_null_consent_are_rejected(self):
        for value in ['missing', False, None]:
            data = {'name': 'Test', 'email': 'test@example.com', 'message': 'Hello'}
            if value != 'missing':
                data['consent_accepted'] = value
            response = self.client.post('/api/contact/', data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn('consent_accepted', response.data['errors'])
        self.assertFalse(ContactRequest.objects.exists())
