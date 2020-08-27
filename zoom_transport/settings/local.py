
from . base import *

#DEBUG = config('DEBUG', default=False, cast=bool)

DEBUG = True

# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zoom_db',
        'USER': 'root',
        'PASSWORD': 'zoom@2020',
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail42.lwspanel.com'
EMAIL_HOST_USER = 'direction@zoomtransport-togo.com'
EMAIL_HOST_PASSWORD = 'Zoomtransp@2020'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
