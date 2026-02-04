from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -------------------
# BASE CONFIG
# -------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-d-0=c^6$e9*4as$tr#16vh!11cx)(&wf&qz&kkl=awwgb)-qec"
)

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# -------------------
# INSTALLED APPS
# -------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App
    'core',

    # Third-party
    'rest_framework',
]

# -------------------
# MIDDLEWARE
# -------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.AttendanceSessionMiddleware',
]

# -------------------
# URL & WSGI
# -------------------
ROOT_URLCONF = 'attendance_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder
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

WSGI_APPLICATION = 'attendance_system.wsgi.application'

# -------------------
# DATABASE
# -------------------
# Option 1: PostgreSQL (Recommended for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'attendance_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Option 2: SQLite (Original - for development)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# -------------------
# PASSWORD VALIDATION
# -------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------
# INTERNATIONALIZATION
# -------------------
LANGUAGE_CODE = 'en-gb'  # Changed to British English for DD/MM/YYYY date format
TIME_ZONE = 'Asia/Kolkata'  # Set to Indian Standard Time (IST)
USE_I18N = True
USE_TZ = True

# Date format settings for DD/MM/YYYY (commented out - reverted to defaults)
# DATE_FORMAT = 'd/m/Y'
# DATETIME_FORMAT = 'd/m/Y H:i:s'
# SHORT_DATE_FORMAT = 'd/m/Y'

# -------------------
# STATIC & MEDIA
# -------------------
STATIC_URL = '/static/'
# -------------------
# STATIC & MEDIA
# -------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT = BASE_DIR / "staticfiles"

# === MEDIA FILES CONFIGURATION (FOR UPLOADS/IMAGES) ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# ======================================================

# -------------------
# DEFAULTS
# -------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------
# EMAIL CONFIG
# -------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "123anfas@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -------------------
# AUTH & LOGIN/LOGOUT
# -------------------
AUTH_USER_MODEL = 'core.User'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'
