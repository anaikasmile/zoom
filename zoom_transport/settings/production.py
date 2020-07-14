#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zoomdb',
        'USER': 'postgres',
        'PASSWORD': '@Azerty2020',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['91.234.195.225', 'localhost', '127.0.0.1']
#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEBUG = False
