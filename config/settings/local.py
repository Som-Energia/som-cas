from .base import *


ALLOWED_HOSTS = [
    'localhost',
]

db_conf = config['databases']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_conf['som_cas']['name'],
        'USER': db_conf['som_cas']['user'],
        'PASSWORD': db_conf['som_cas']['password'],
        'HOST': db_conf['som_cas']['host'],
        'PORT': db_conf['som_cas']['port']
    },
    'users_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_conf['users_db']['name'],
        'USER': db_conf['users_db']['user'],
        'PASSWORD': db_conf['users_db']['password'],
        'HOST': db_conf['users_db']['host'],
        'PORT': db_conf['users_db']['port']
    }
}

RQ_QUEUES = config['queues']

TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'django.template.context_processors.debug'
)

erp_conf = config['erp']
ERP = {
    'user': erp_conf.get('user'),
    'password': erp_conf.get('password'),
    'db': erp_conf.get('db'),
    'server': erp_conf.get('server'),
}


MAMA_CAS_SERVICES = config.get('mama_cas_services', [])

MAMA_CAS_SERVICE_BACKENDS = [
    'mama_cas.services.backends.SettingsBackend'
]

MAMA_CAS_FOLLOW_LOGOUT_URL = True

CUSTOM_REGISTRATION_SERVICES = config.get('custom_registration_services', '')

REGISTRATION_SERVICES = config.get('registration_services', '')

UPLOAD_DIR = 'registered_members'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
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
