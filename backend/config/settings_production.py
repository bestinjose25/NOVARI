"""Production settings; missing deployment configuration is a startup error."""
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

from .settings import *


def required(name):
    value = os.environ.get(name, '').strip()
    if not value:
        raise ImproperlyConfigured(f'{name} must be set for production.')
    return value


DEBUG = False
SECRET_KEY = required('SECRET_KEY')
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5 or SECRET_KEY.startswith('django-insecure-'):
    raise ImproperlyConfigured('Generate a strong production SECRET_KEY.')

ALLOWED_HOSTS = [value.strip() for value in required('ALLOWED_HOSTS').split(',') if value.strip()]
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('ALLOWED_HOSTS must list explicit backend hostnames.')

DATABASE_URL = required('DATABASE_URL')
if urlparse(DATABASE_URL).scheme not in ('postgres', 'postgresql'):
    raise ImproperlyConfigured('Production requires PostgreSQL.')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=60, conn_health_checks=True)}

CORS_ALLOWED_ORIGINS = [value.strip() for value in required('CORS_ALLOWED_ORIGINS').split(',') if value.strip()]
SITE_URL = required('SITE_URL').rstrip('/')
for origin in [*CORS_ALLOWED_ORIGINS, SITE_URL]:
    parsed = urlparse(origin)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.path or parsed.query or parsed.fragment:
        raise ImproperlyConfigured('Production origins must be HTTPS URLs without paths or trailing slashes.')
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys([SITE_URL, *CORS_ALLOWED_ORIGINS]))

MEDIA_ROOT = Path(required('MEDIA_ROOT'))
if not MEDIA_ROOT.is_absolute():
    raise ImproperlyConfigured('MEDIA_ROOT must be an absolute persistent-disk path.')
EMAIL_HOST_USER = required('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = required('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = required('DEFAULT_FROM_EMAIL')
NOVARI_NOTIFICATION_EMAIL = required('NOVARI_NOTIFICATION_EMAIL')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'
# Render health probes may use HTTP internally; no business data is returned.
SECURE_REDIRECT_EXEMPT = [r'^health/$']

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.AnonRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'anon': '10/hour'},
    'NUM_PROXIES': 1,
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'quotes': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'contacts': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    },
}
