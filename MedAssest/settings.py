"""
Django settings for MedAssest project.
Optimized for Production (Render) and Local Development.
"""
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file for local development
load_dotenv(BASE_DIR / '.env')

# ==========================================
# SECURITY SETTINGS (CRITICAL)
# ==========================================
# Raises an error if SECRET_KEY is missing in production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-@!s9!0p2-%(4c5av9vz=doo=cqdh=3(f*#m27ntnotew2iea+m')

# Strictly False in production unless explicitly set in environment
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Allow all hosts temporally. Restrict this to Render domain later.
ALLOWED_HOSTS = ["*"]

# ==========================================
# CORS & INTEGRATION
# ==========================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://charity-fund-frontend.vercel.app",
]

# ==========================================
# APPLICATION DEFINITION
# ==========================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'users',
    'patients',
    'aid_providers',
    'aid_requests',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Required for serving static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MedAssest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'MedAssest.wsgi.application'

# ==========================================
# DATABASE SETTINGS
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(
        os.environ.get('DATABASE_URL'), 
        ssl_require=True
    )

if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(
        os.environ.get('DATABASE_URL'), 
        ssl_require=True
    )

# ==========================================
# PASSWORD VALIDATION
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==========================================
# INTERNATIONALIZATION
# ==========================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================
# STATIC FILES (CSS, JavaScript, Images)
# ==========================================
STATIC_URL = 'static/'
# CRITICAL FOR RENDER: Defines where collectstatic drops the files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Optional: Enable WhiteNoise compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==========================================
# DEFAULT PRIMARY KEY
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# ==========================================
# REST FRAMEWORK & JWT SETTINGS
# ==========================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}