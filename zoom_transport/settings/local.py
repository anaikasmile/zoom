
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