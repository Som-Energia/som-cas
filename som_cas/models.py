from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


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

    def __repr__(self):
        return f'<AgRegistration({self.assembly.name}, {self.member.username})>'

    def __str__(self):
        return self.__repr__()

