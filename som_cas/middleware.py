from django.utils import translation


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
