import logging

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from .utils import send_confirmation_email, is_company

logger = logging.getLogger('models')


class RegistrationChoices:

    INPERSON = 'in_person'
    VIRTUAL = 'virtual'

    choices = (
        (INPERSON, _('In person')),
        (VIRTUAL, _('Virtual')),
    )


class SomUser(AbstractUser):
    """
    User definition for our autentication service
    """

    lang = models.CharField(max_length=10, blank=True, null=True)

    www_phone = models.CharField(max_length=64, blank=True, null=True)

    www_mobile = models.CharField(max_length=64, blank=True, null=True)

    www_soci = models.IntegerField(blank=True, null=True)

    def __repr__(self):
        return '<SomUser(username={}, soci={})>'.format(
            self.username, self.www_soci
        )

    def __str__(self):
        return self.__repr__()

    def isVirtualRegisteredInActiveAssembly(self):
        registry = AgRegistration.objects.filter(
            member=self,
            assembly__active=True,
            registration_type=RegistrationChoices.VIRTUAL,
        )
        return registry.exists()

    def registerInVirtualAssembly(self):
        assembly = (Assembly.objects.filter(active=True) or [None])[0]
        if not assembly: return None

        registration, created = AgRegistration.objects.get_or_create(
            member=self,
            assembly=assembly,
            defaults=dict(
                registration_type=RegistrationChoices.VIRTUAL,
            ),
        )
        if registration.registration_type == RegistrationChoices.INPERSON:
            return None

        if created:
            try:
                send_confirmation_email.delay(self, 'som_cas/mail_confirmation.html')
                registration.registration_email_sent = True
                registration.save()
            except Exception as e:
                msg = "Confirmation email not sent due to '%s':"
                logger.error(msg, e)
        return registration

    def full_name(self):
        if not is_company(self.username):
            return f'{self.first_name} {self.last_name}'
        else:
            if not self.last_name:
                return f'{self.first_name}'
            return f'{self.last_name} {self.first_name}'


class Assembly(models.Model):
    """
    Assembly definition
    """
    name = models.CharField(
        max_length=150,
        unique_for_year="date",
        verbose_name=_('Assembly name'),
        help_text=_('Name of the assembly, eg: Asamblea 2020')
    )

    registered = models.ManyToManyField(
        SomUser,
        through='AgRegistration',
        through_fields=('assembly', 'member'),
    )

    date = models.DateField(
        verbose_name=_("Start time"),
        help_text=_("Date when this occurrence end")
    )

    active = models.BooleanField(
        verbose_name=('Active'),
        help_text=_('Assembley state')
    )

    def __repr__(self):
        return f'<Assembly({self.name})>'

    def __str__(self):
        return self.__repr__()


class AgRegistration(models.Model):

    assembly = models.ForeignKey(
        Assembly,
        on_delete=models.CASCADE,
        verbose_name=_('Assembly'),
        help_text=_('Assembly for this registration')
    )

    member = models.ForeignKey(
        SomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Member'),
        help_text=_('Member for this registration')
    )

    date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Registration date'),
        help_text=_('Member registration date')
    )

    registration_type = models.CharField(
        max_length=15,
        choices=RegistrationChoices.choices,
        verbose_name=_('Registration type'),
        help_text=_('Type of registration: if virtual or in person')
    )

    registration_email_sent = models.BooleanField(
        default=False,
        verbose_name=_('Sent registration email'),
        help_text=_('Check if registration email was sent to the member')
    )

    def __repr__(self):
        return f'<AgRegistration({self.assembly.name}, {self.member.username})>'

    def __str__(self):
        return self.__repr__()

# vim: et ts=4 sw=4
