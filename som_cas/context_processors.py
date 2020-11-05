import re

from django.conf import settings

from som_cas.models import Assembly

URL_REGEX = re.compile('https?://(?P<service>\w+\.somenergia\.coop)')


def service_context_processors(request):
    service = URL_REGEX.search(request.GET.get('service', ''))
    if not service:
        return ''

    service = service.groupdict()['service']
    context = {
        'serviceName': settings.REGISTRATION_SERVICES.get(
            service, {}
        ).get('service_name', '')
    }
    if settings.CUSTOM_REGISTRATION_SERVICES in service:
        context['assembly'] = Assembly.assemblies.get_active_assembly()

    return context
