import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'valore-default-non-sicuro-da-usare-solo-se-manca-env')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

allowed_hosts_string = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_string.split(',') if host.strip()]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export', # Per django-import-export
    'inventory.apps.InventoryConfig', # Modo esplicito di registrare la tua app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Assicurati che questo percorso sia corretto per il tuo base.html
        # Se base.html è in app/config/templates, allora è BASE_DIR / 'config' / 'templates'
        # Se base.html è in app/templates, allora è BASE_DIR / 'templates'
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Dove collectstatic mette i file

STATICFILES_DIRS = [
    BASE_DIR / 'static', # Dice a Django di cercare file statici anche nella directory 'static' alla radice dell'app Django (BASE_DIR)
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django-import-export settings (opzionale)
IMPORT_EXPORT_USE_TRANSACTIONS = True

# AUTHENTICATION SETTINGS
LOGIN_URL = 'login'  # Nome dell'URL pattern per la vista di login
LOGIN_REDIRECT_URL = 'inventory:inventory_list' # Dove reindirizzare dopo login (assumendo che 'inventory_list' sia la tua lista principale nell'app 'inventory')
LOGOUT_REDIRECT_URL = 'login' # Dove reindirizzare dopo il logout

# CRISPY FORMS (se non già impostato bene)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Raccolta per la produzione
STATICFILES_DIRS = [
    BASE_DIR / "static", # La tua cartella 'app/static'
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles' # Dove vengono caricati i file (es. foto profili)

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# DJANGO IMPORT EXPORT
IMPORT_EXPORT_USE_TRANSACTIONS = True # Buona pratica

# AUTHENTICATION SETTINGS
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inventory:home_inventory' # Reindirizza alla home dell'inventario dopo il login
LOGOUT_REDIRECT_URL = 'login' # Reindirizza alla pagina di login dopo il logout

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Per testare email in console