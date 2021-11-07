from karsoogh.settings.base import *
import sys

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*z!3aidedw32xh&1ew(^&5dgd17(ynnmk=s*mo=v2l_(4t_ff('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('db.sqlite3'),
    }
}

TESTING = sys.argv[1] == 'test'

STATIC_ROOT = get_environment_var('STATIC_ROOT', 'staticfiles')
MEDIA_ROOT = get_environment_var('MEDIA_ROOT', 'media')
