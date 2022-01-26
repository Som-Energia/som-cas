import re

from django.conf import settings

from som_cas.models import Assembly

URL_REGEX = re.compile(r'https?://(?P<service>[\w-]+\.([\w-]+\.)*somenergia\.coop)')


def service_context_processors(request):
    service = URL_REGEX.search(request.GET.get('service', ''))
    if not service:
        return ''

    service_name = settings.REGISTRATION_SERVICES.get(
        service.groupdict()['service'], {}
    ).get('service_name', '')
    context = {
        'service_name': service_name
    }
    if service_name == 'ASSEMBLEA':
        context['assembly'] = Assembly.assemblies.get_forthcoming_assembly()

    return context
