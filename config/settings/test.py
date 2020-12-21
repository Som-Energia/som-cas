from django.core.exceptions import ImproperlyConfigured

from .base import *

CONFIG_FILE = os.path.join(str(BASE_DIR), 'som_cas/tests/test.conf.yaml')

try:
    with open(str(CONFIG_FILE), 'r') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
except FileNotFoundError:
    msg = 'Configuration file {} is not defined'
    raise ImproperlyConfigured(msg.format(str(CONFIG_FILE)))

DEBUG = True

SECRET_KEY = config['secret_key']

ALLOWED_HOSTS = config.get('allowed_hosts', [])

UPLOAD_DIR = config['upload_dir']

db_conf = config['databases']
if not db_conf.get('users_db', False):
    raise ImproperlyConfigured('users_db configuration is not defined')
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

erp_conf = config['erp']
ERP = {
    'user': erp_conf.get('user'),
    'password': erp_conf.get('password'),
    'db': erp_conf.get('db'),
    'server': erp_conf.get('server'),
}

RQ_QUEUES = config['queues']

MAMA_CAS_SERVICES = config.get('mama_cas_services', [])

MAMA_CAS_SERVICE_BACKENDS = [
    'mama_cas.services.backends.SettingsBackend'
]

MAMA_CAS_LOGIN_TEMPLATE = 'som_cas/login.html'

MAMA_CAS_FOLLOW_LOGOUT_URL = True

REGISTRATION_SERVICES = config.get('registration_services', '')

logging_conf = config['logging']

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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'som_cas.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
        'mama_cas': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        },
        'som_cas': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
