import logging
from threading import local
from urllib import parse

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from som_cas import utils

_thread_locals = local()

logger = logging.getLogger(__name__)


class CasRedirectMiddleware(object):
    """
    Middleware to detect redirections in service url
    """

    def get_redirect_url(self, request):
        service = request.GET.get('service', '')
        parsed_service = parse.urlparse(service)
        return parse.parse_qs(parsed_service.query).get('redirect_to')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = self.get_redirect_url(request)
        if redirect_url:
            request.GET = request.GET.copy()
            request.GET['service'] = redirect_url[0]

        response = self.get_response(request)
        return response


class CasLanguageMiddleware(object):
    """
    Custom middleware to enable custom language in CAS login view
    """

    language_param = 'locale'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if self.language_param in request.GET:
            translation.activate(request.GET[self.language_param])
            request.LANGUAGE_CODE = translation.get_language()

        response = self.get_response(request)

        return response


def _set_erp_connection(erp_con_func):
    setattr(_thread_locals, '_erp_con', erp_con_func.__get__(erp_con_func, local))


def get_erp_con():
    current_erp_con = getattr(_thread_locals, '_erp_con', None)
    if callable(current_erp_con):
        return current_erp_con()
    return current_erp_con


class ERPClientMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _set_erp_connection(
            lambda self: utils.ErpClientManager.get_erp_client_instance()
        )
        response = self.get_response(request)
        return response


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = utils.get_user(request)
    return request._cached_user


class SomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE%s setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        ) % ("_CLASSES" if settings.MIDDLEWARE is None else "")
        request.user = SimpleLazyObject(lambda: get_user(request))
