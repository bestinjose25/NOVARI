from .settings import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
EMAIL_BACKEND = ('django.core.mail.backends.smtp.EmailBackend'
                 if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
                 else 'django.core.mail.backends.filebased.EmailBackend')
EMAIL_FILE_PATH = BASE_DIR / '.local-emails'
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL or EMAIL_HOST_USER or 'local@novari.test'
CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']
SITE_URL = 'http://127.0.0.1:8001'

