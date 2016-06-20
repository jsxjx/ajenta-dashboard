import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'bootstrapform',
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

ROOT_URLCONF = 'django_ajenta_dashboard.urls'

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

WSGI_APPLICATION = 'django_ajenta_dashboard.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'users.sqlite3'),
    },
    'ajenta_io': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal2',
        'USER': os.environ['AJENTA_DATABASE_NAME'],
        'PASSWORD': os.environ['AJENTA_DATABASE_PASSWORD'],
        'HOST': os.environ['AJENTA_DATABASE_HOST'],
    },
    'platformc': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portal2',
        'USER': os.environ['OYDIV_DATABASE_NAME'],
        'PASSWORD': os.environ['OYDIV_DATABASE_PASSWORD'],
        'HOST': os.environ['OYDIV_DATABASE_HOST'],
    },
}

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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Login URL
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'

# HTTPS security
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

# Static files
STATIC_URL = '/static/'

STATIC_PATH = os.path.join(BASE_DIR, 'static')

STATIC_ROOT = "/var/www/dashboard.ajenta.io/static/"

STATICFILES_DIRS = (
    STATIC_PATH,
)
