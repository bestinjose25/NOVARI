from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import os
import dj_database_url

# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-change-this-later'
)

DEBUG = (
    os.getenv(
        'DEBUG',
        'True'
    ).lower()
    == 'true'
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        'ALLOWED_HOSTS',
        '127.0.0.1,localhost'
    ).split(',')
    if host.strip()
]


# ---------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',

    'contacts.apps.ContactsConfig',
    'quotes.apps.QuotesConfig',
]


# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ---------------------------------------------------------
# URL CONFIGURATION
# ---------------------------------------------------------

ROOT_URLCONF = 'config.urls'


# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

            'DIRS': [
                BASE_DIR / 'templates',
            ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ---------------------------------------------------------
# WSGI
# ---------------------------------------------------------

WSGI_APPLICATION = 'config.wsgi.application'


# ---------------------------------------------------------
# DATABASE - POSTGRESQL
# ---------------------------------------------------------

DATABASE_URL = os.getenv('DATABASE_URL')


if DATABASE_URL:

    # Neon / hosted PostgreSQL
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=30,
            ssl_require=True,
        )
    }

else:

    # Local PostgreSQL fallback
    DATABASES = {
        'default': {
            'ENGINE':
                'django.db.backends.postgresql',

            'NAME':
                os.getenv('DB_NAME'),

            'USER':
                os.getenv('DB_USER'),

            'PASSWORD':
                os.getenv('DB_PASSWORD'),

            'HOST':
                os.getenv(
                    'DB_HOST',
                    '127.0.0.1'
                ),

            'PORT':
                os.getenv(
                    'DB_PORT',
                    '5432'
                ),
        }
    }


# ---------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ---------------------------------------------------------
# LANGUAGE / TIMEZONE
# ---------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_TZ = True


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'
# ---------------------------------------------------------
# DEFAULT PRIMARY KEY
# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:5173'
    ).split(',')
    if origin.strip()
]


# -----Media-----


MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# -----Media-----


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv(
    'EMAIL_HOST',
    'smtp.gmail.com'
)

EMAIL_PORT = int(
    os.getenv(
        'EMAIL_PORT',
        '587'
    )
)

EMAIL_HOST_USER = os.getenv(
    'EMAIL_HOST_USER'
)

EMAIL_HOST_PASSWORD = os.getenv(
    'EMAIL_HOST_PASSWORD'
)

EMAIL_USE_TLS = (
    os.getenv(
        'EMAIL_USE_TLS',
        'True'
    ).lower()
    == 'true'
)

EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = os.getenv(
    'DEFAULT_FROM_EMAIL',
    EMAIL_HOST_USER
)

NOVARI_NOTIFICATION_EMAIL = os.getenv(
    'NOVARI_NOTIFICATION_EMAIL',
    'bestinjoseofficial@gmail.com'
)

EMAIL_TIMEOUT = 15


SITE_URL = os.getenv(
    'SITE_URL',
    'http://127.0.0.1:8001'
)


SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)