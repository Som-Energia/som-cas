import logging
import re

from django.conf import settings
from django.contrib import auth
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _, override
from django_rq import job


logger = logging.getLogger('rq.worker')

def get_user(request):
    user = auth.get_user(request)

    if isinstance(user, auth.models.AnonymousUser):
        return user

    if settings.CUSTOM_REGISTRATION_SERVICES in request.GET.get('service', ''):
        if user.isVirtualRegisteredInActiveAssembly():
            return user
        return auth.models.AnonymousUser()

    return user


@job('email_queue')
def send_confirmation_email(user, email_template):
    from som_cas.models import AgRegistration

    try:
        user_registration = AgRegistration.objects.get(
            member=user,
            assembly__active=True,
            registration_email_sent=False
        )
    except ObjectDoesNotExist:
        logger.info(f"Confirmation email has been sent already to {user}")
    else:
        with override(user.lang):
            msg = EmailMessage(
                _('Confirmació d’Inscripció a la Assemblea'),
                render_to_string(email_template, {'user': user}),
                '',
                [user.email],
                settings.BCC,
            )
            msg.content_subtype = "html"
            msg.send()

        user_registration.registration_email_sent = True
        user_registration.save()


def getActiveAssembly():
    from som_cas.models import Assembly
    return (Assembly.objects.filter(active=True) or [None])[0]


def service_context_processors(request):
    service = request.GET.get('service', '')
    pattern = "\w*\.somenergia\.coop"
    registrate_service = re.search(pattern, service).group()

    context = {
        'serviceName': settings.REGISTRATION_SERVICES.get(registrate_service).get('service_name')
    }
    if settings.CUSTOM_REGISTRATION_SERVICES in service:
        context['assembly'] = getActiveAssembly()

    return context

def is_company(vat):
    if vat:
        return vat[0] not in '0123456789KLMXYZ'
# vim: noet ts=4 sw=4
