"""
Django settings for clothing_business_project project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-%dr&$d965qy3s0ms^vs-f4jm98e*4cus3rtm+wap3z-_(y$4*8')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
HOSTINGER_HOST = os.environ.get('HOSTINGER_HOST', '').strip()
if HOSTINGER_HOST:
    ALLOWED_HOSTS.extend([host.strip() for host in HOSTINGER_HOST.split(',') if host.strip()])


# ── Apps ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'mainapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clothing_business_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clothing_business_project.wsgi.application'


# ── Database ──────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ── Password validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
# ── Media & Static storage ───────────────────────────────────────────────────
# cloudinary://API_KEY:API_SECRET@CLOUD_NAME
_CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '').strip()
_CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '').strip()
_CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '').strip()
_CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '').strip()
_USE_CLOUDINARY = bool(
    _CLOUDINARY_URL or (
        _CLOUDINARY_CLOUD_NAME and _CLOUDINARY_API_KEY and _CLOUDINARY_API_SECRET
    )
)

if _USE_CLOUDINARY:
    import re as _re
    import cloudinary as _cld
    if _CLOUDINARY_URL:
        _m = _re.match(r'cloudinary://([^:]+):([^@]+)@(.+)', _CLOUDINARY_URL)
        if _m:
            _cld.config(
                cloud_name=_m.group(3).strip(),
                api_key=_m.group(1).strip(),
                api_secret=_m.group(2).strip(),
            )
    else:
        _cld.config(
            cloud_name=_CLOUDINARY_CLOUD_NAME,
            api_key=_CLOUDINARY_API_KEY,
            api_secret=_CLOUDINARY_API_SECRET,
        )
    # Custom storage backend — no django-cloudinary-storage needed
    STORAGES = {
        'default': {
            'BACKEND': 'clothing_business_project.cloudinary_backend.CloudinaryMediaStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
    MEDIA_URL = '/media/'
else:
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# ── Authentication ────────────────────────────────────────────────────────────
LOGIN_URL = '/user_login'
LOGIN_REDIRECT_URL = '/user_dashboard'

# ── Session ───────────────────────────────────────────────────────────────────
SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ── Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# File Upload Limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760   # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760   # 10 MB

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
