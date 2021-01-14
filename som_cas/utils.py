import locale
import logging
from contextlib import contextmanager
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import auth
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.translation import gettext as _, override
from django_rq import job
from erppeek import Client


logger = logging.getLogger('rq.worker')


def is_assembly_service(service):
    service = urlparse(service).netloc.split(':')[0]
    service_name = settings.REGISTRATION_SERVICES.get(
        service, {}
    ).get('service_name', '')

    return service_name == 'ASSAMBLEA'


def get_user(request):
    user = auth.get_user(request)

    if isinstance(user, auth.models.AnonymousUser):
        return user

    if is_assembly_service(request.GET.get('service', '')):
        if user.is_registered_in_active_virtual_assembly():
            return user
        return auth.models.AnonymousUser()

    return user


@job('email_queue')
def send_confirmation_email(member, email_template):
    from som_cas.models import AgRegistration

    try:
        registration = AgRegistration.registrations.registration_with_pending_email_confirmation(member)
    except ObjectDoesNotExist:
        logger.info(f"There is no pending registration to confirm for {member}")
    else:
        with override(member.lang):
            context = {
                'member': member,
                'assembly': registration.assembly
            }
            subject = _("Confirmació d'inscripció {}".format(registration.assembly.local_group.alias)) if registration.assembly.local_group is not None else _('Confirmació d’inscripció a la Assemblea')
            msg = EmailMessage(
                subject,
                render_to_string(email_template, context),
                '',
                [member.email],
                settings.BCC,
            )
            msg.content_subtype = "html"
            msg.send()

        registration.registration_email_sent = True
        registration.save()


def is_company(vat):
    if vat:
        return vat[0] not in '0123456789KLMXYZ'


@contextmanager
def locale_override(locale_name):
    LOCALE_MAPPING = {
        'es': ('es', 'UTF-8'),
        'ca': ('ca', 'UTF-8'),
        'eu': ('eu', 'UTF-8'),
        'ga': ('ga', 'UTF-8'),
        'en': ('en', 'UTF-8')
    }
    loc = locale.getlocale()

    try:
        yield locale.setlocale(
            locale.LC_ALL, LOCALE_MAPPING.get(locale_name, ('ca', 'UTF-8'))
        )
    finally:
        locale.setlocale(locale.LC_ALL, loc)


class ErpClientManager(object):
    _client = None
    _logger = logging.getLogger(__name__)

    @classmethod
    def get_erp_client_instance(cls):
        if cls._client is None:
            cls._client = Client(**settings.ERP)
            msg = 'Connected to ERP username: %s, server: %s'
            cls._logger.info(msg, settings.ERP['user'], settings.ERP['server'])
        return cls._client


# vim: noet ts=4 sw=4
