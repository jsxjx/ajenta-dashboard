import os
import getpass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '+#m=cxemg90avd4^$vzeve=w73l@od84#0$9ft6(f1!0#+roc#'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'dashboard',
    'bootstrap3',
    'datetimewidget',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ajenta_dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

BOOTSTRAP3 = {
    'success_css_class': '',
}

WSGI_APPLICATION = 'ajenta_dashboard.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'users.sqlite3'),
    },
    'ajenta.io': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal2',
        'USER': os.environ.get('AJENTA_DATABASE_NAME', 'cdraccess'),
        'PASSWORD': os.environ.get('AJENTA_DATABASE_PASSWORD', getpass.getpass(prompt='Ajenta.io password:')),
        'HOST': os.environ.get('AJENTA_DATABASE_HOST'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
    'platformc': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal2',
        'USER': os.environ.get('OYDIV_DATABASE_NAME', 'cdraccess'),
        'PASSWORD': os.environ.get('OYDIV_DATABASE_PASSWORD', getpass.getpass(prompt='Platformc password:')),
        'HOST': os.environ.get('OYDIV_DATABASE_HOST'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    },
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'GB'

USE_I18N = False

USE_L10N = False

USE_TZ = False

DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y/%m/%d')

# Login URL
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATIC_ROOT = os.path.join(STATIC_PATH, 'dashboard_static')

STATICFILES_DIRS = (
    STATIC_PATH,
)
