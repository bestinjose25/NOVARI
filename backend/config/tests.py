from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase


class HealthTests(TestCase):
    def test_health_checks_database_without_exposing_configuration(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
        self.assertEqual(response['Cache-Control'], 'no-store')

    @patch('config.views.connection.cursor', side_effect=DatabaseError('private connection details'))
    def test_failure_returns_only_generic_status(self, _cursor):
        with self.assertLogs('config.views', level='ERROR'):
            response = self.client.get('/health/')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unavailable'})

    def test_health_does_not_accept_post(self):
        self.assertEqual(self.client.post('/health/').status_code, 405)


class UploadBudgetTests(TestCase):
    def test_upload_budget_is_shared_across_files(self):
        from django.core.exceptions import RequestDataTooBig
        from django.test import override_settings
        from .uploads import UploadBudgetHandler
        with override_settings(MAX_QUOTE_UPLOAD_BYTES=10):
            handler = UploadBudgetHandler()
            self.assertEqual(handler.receive_data_chunk(b'123456', 0), b'123456')
            handler.file_complete(6)
            with self.assertRaises(RequestDataTooBig):
                handler.receive_data_chunk(b'12345', 0)


class ProductionSettingsTests(TestCase):
    def run_settings(self, **changes):
        import os
        import subprocess
        import sys
        from pathlib import Path
        env = os.environ.copy()
        env.update(DJANGO_SETTINGS_MODULE='config.settings_production',
            SECRET_KEY='production-test-key-only-' + 'abcdefgh1234567890' * 4,
            ALLOWED_HOSTS='api.example.de', DATABASE_URL='postgresql://test:unused@localhost/test',
            CORS_ALLOWED_ORIGINS='https://example.de', SITE_URL='https://api.example.de',
            MEDIA_ROOT=str(Path(__file__).resolve().parent.parent / 'media'),
            EMAIL_HOST_USER='test@example.de', EMAIL_HOST_PASSWORD='unused-test-password',
            DEFAULT_FROM_EMAIL='test@example.de', NOVARI_NOTIFICATION_EMAIL='owner@example.de')
        env.update(changes)
        return subprocess.run([sys.executable, '-c',
            "import django; django.setup(); from django.conf import settings; "
            "assert settings.DEBUG is False; assert settings.SESSION_COOKIE_SECURE; "
            "assert settings.CSRF_COOKIE_SECURE; assert settings.SECURE_SSL_REDIRECT; "
            "print(settings.DATABASES['default'].get('OPTIONS', {}).get('sslmode', 'internal'))"],
            cwd=Path(__file__).resolve().parent.parent, env=env, capture_output=True, text=True)

    def test_secure_defaults_and_internal_database_url(self):
        result = self.run_settings()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'internal')

    def test_external_database_ssl_parameter_is_preserved(self):
        result = self.run_settings(DATABASE_URL='postgresql://test:unused@localhost/test?sslmode=require')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'require')

    def test_missing_secrets_wildcard_hosts_and_http_origins_fail_closed(self):
        for change in [{'SECRET_KEY': ''}, {'SECRET_KEY': 'short'}, {'DATABASE_URL': ''},
                       {'ALLOWED_HOSTS': '*'}, {'CORS_ALLOWED_ORIGINS': 'http://example.de'},
                       {'EMAIL_HOST_PASSWORD': ''}]:
            with self.subTest(change=list(change)):
                result = self.run_settings(**change)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('ImproperlyConfigured', result.stderr)
