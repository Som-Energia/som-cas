from .base import *


ALLOWED_HOSTS = [
    'cas.somenergia.coop'
]

MAMA_CAS_SERVICES = [
    {
        'SERVICE': '^https://participa\.somenergia\.coop[\]?.*',
        'CALLBACKS': [
            'som_cas.callbacks.participa',
        ],
        'LOGOUT_ALLOW': True,
        'LOGOUT_URL': 'https://participa.somenergia.coop/logout',
        'PROXY_ALLOW': True,
        'PROXY_PATTERN': '^https://participa\.somenergia\.coop',
    }

]

MAMA_CAS_SERVICE_BACKENDS = [
    'mama_cas.services.backends.SettingsBackend'
]

MAMA_CAS_LOGIN_TEMPLATE = 'som_cas/login.html'
