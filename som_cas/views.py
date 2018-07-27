import logging
from urllib.parse import urlparse, parse_qsl

from django.contrib.auth import login
from django.http import JsonResponse

from mama_cas.views import LoginView
from mama_cas.models import ServiceTicket
from mama_cas.utils import redirect

logger = logging.getLogger('som_cas')


def get_ticket(url):
    parsed_url = urlparse(url)
    return dict(parse_qsl(parsed_url.query))


def get_service(url):
    return urlparse(url).netloc


def build_response_data(url):
    response_data = {
        'service': get_service(url)
    }
    response_data.update(get_ticket(url))

    return response_data


class SomLoginView(LoginView):

    def form_valid(self, form):
        response = super().form_valid(form)

        if 'application/json' in self.request.META['HTTP_ACCEPT'].split(','):
            response_data = build_response_data(response.url)
            response = JsonResponse(response_data)

        return response
