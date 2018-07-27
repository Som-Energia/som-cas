from .base import *

ALLOWED_HOSTS = [
    'localhost',
    'cas.somenergia.coop'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kasko_db',
        'USER': 'kasko',
        'PASSWORD': '4321',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'users_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'somdb',
        'USER': 'usom',
        'PASSWORD': '4321',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'django.template.context_processors.debug'
)
