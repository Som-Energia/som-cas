from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from som_cas import utils


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

