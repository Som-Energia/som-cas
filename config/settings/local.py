from .base import *


ALLOWED_HOSTS = [
    'localhost',
    'cas.somenergia.coop'
]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

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


MAMA_CAS_SERVICES = [
    {
        'SERVICE': r'^http[s]?://participa\.somenergia\.coop:8080[/]?.*',
        'CALLBACKS': [
            'som_cas.callbacks.participa',
        ],
        'LOGOUT_ALLOW': True,
        'LOGOUT_URL': 'http://participa.somenergia.coop:8080/logout',
        'PROXY_ALLOW': False,
        'PROXY_PATTERN': r'^http[s]?://participa\.somenergia\.coop:8080',
    }
]

MAMA_CAS_SERVICE_BACKENDS = [
    'mama_cas.services.backends.SettingsBackend'
]

MAMA_CAS_LOGIN_TEMPLATE = 'som_cas/login.html'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'filters': {
    #     'require_debug_false': {
    #         '()': 'django.utils.log.RequireDebugFalse'
    #     }
    # },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s]'
                      '[%(module)s.%(funcName)s:%(lineno)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'som_cas': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'mama_cas': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
