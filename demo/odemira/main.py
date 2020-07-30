import base64
import os
import logging
import logging.config
from concurrent.futures import ThreadPoolExecutor
from cryptography import fernet
from functools import partial

import aiohttp_jinja2
import cas
import jinja2
from aiohttp import web

from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s]'
                      '[%(module)s.%(funcName)s:%(lineno)s] %(message)s'
        },
        'access': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'access': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'access'
        }
    },
    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'aiohttp.access': {
            'handlers': ['access'],
            'level': 'DEBUG',
            'propagate': True
        },
        'aiohttp.server': {
            'handlers': ['access'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger('main')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

CAS_SERVER_URL = 'http://localhost:8000/'

SERVICE_NAME = 'http://odemira.somenergia.coop:6994'


@web.middleware
async def cas_middleware(request, handler):
    if request.query.get('ticket'):
        username, user, _ = await request.loop.run_in_executor(
            ThreadPoolExecutor(),
            partial(
                request.app['cas_client'].verify_ticket,
                ticket=request.query.get('ticket')
            )
        )
        logger.debug("%s, %s, %s", username, user, _)
        request.user = user
        session = await get_session(request)
        session['user'] = user
    else:
        session = await get_session(request)
        request.user = session.get('user', {})

    response = await handler(request)

    return response


async def index(request):
    login_url = request.app['cas_client'].get_login_url()

    context = {
        'request': request,
        'login_url': login_url
    }
    return aiohttp_jinja2.render_template('index.html', request, context)


async def welcome(request):
    if hasattr(request, 'user') and request.user:
        login_url = request.app['cas_client'].get_login_url()

        context = {
            'request': request,
            'login_url': login_url
        }
        return aiohttp_jinja2.render_template('welcome.html', request, context)

    return aiohttp_jinja2.render_template('404.html', request, {}, status=404)


def setup_routes(app):
    app.router.add_get('/', index)

    app.router.add_get('/welcome', welcome)

    app.router.add_static(
        '/static/',
        path=os.path.join(PROJECT_ROOT, 'static'),
        name='static'
    )


def setup_app():
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    app = web.Application(
        debug=True,
        middlewares=[
            session_middleware(EncryptedCookieStorage(secret_key)),
            cas_middleware
        ]
    )

    app['cas_client'] = cas.CASClientV3(
        server_url=CAS_SERVER_URL,
        service_url=SERVICE_NAME,
        extra_login_params=False,
        renew=False
    )

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(os.path.join(PROJECT_ROOT, 'templates'))
    )

    setup_routes(app)
    return app


app = setup_app()

web.run_app(app, host='localhost', port=6994)
