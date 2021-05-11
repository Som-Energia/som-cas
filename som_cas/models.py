import os
import logging

from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.utils.translation import gettext as _

from .contrib import ERPPartner
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

    def is_registered_in_active_virtual_assembly(self):
        return AgRegistration.registrations.member_in_active_virtual_assembly(self)

    def register_in_virtual_assembly(self):
        assembly = Assembly.assemblies.get_active_assembly_for_member(self)
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

    @property
    def address_codes(self):
        erp_partner = ERPPartner(self.username)
        return erp_partner.address_codes

    @property
    def local_group(self):
        if self.address_codes:
            local_g = LocalGroups.lgs.indentify_member_local_group(
                *self.address_codes
            ).first()
            return local_g.name if local_g else ''

        return ''


class LocalGroupsQuerySet(models.QuerySet):

    def indentify_member_local_group(self, ccaa_code, state_code, city_code):
        query = models.Q(data__alias__city__contains=city_code) | \
            models.Q(data__alias__state__contains=state_code) | \
            models.Q(data__alias__ccaa__contains=ccaa_code)
        return self.filter(query)


class LocalGroups(models.Model):

    def gls_logo_path(instance, filename):
        return os.path.join(
            settings.UPLOAD_DIR,
            '{0}/{1}'.format(instance.name, filename)
        )


    name = models.CharField(
        max_length=128,
        verbose_name=_("Local group name"),
        help_text=_("Name of the local group")
    )
    
    full_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Local group full name"),
        help_text=_("Name of the local group, ex: Grup Local de Girona")
    )

    alias = models.CharField(
        max_length=128,
        blank=True,
        null=True,        
        verbose_name=_("Local group alias name"),
        help_text=_("Alias of the local group, ex: CT Girona")
    )
    
    email = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Local group email"),
        help_text=_("Local group email")
    )

    logo = models.ImageField(
        blank=True,
        null=True,
        upload_to=gls_logo_path,
        verbose_name=_("Local group logo"),
        help_text=_("Logo of the local group")
    )
    
    data = JSONField(
        verbose_name=_("Local group data"),
        help_text=_("Cities, states and provincies related with this local group")
    )

    lgs = LocalGroupsQuerySet.as_manager()

    objects = models.Manager()

    def __str__(self):
        return f'<LocalGroup({self.name})>'

    def __repr__(self):
        return self.__str__()


class AssemblyQuerySet(models.QuerySet):

    def get_active_assembly(self):
        return self.filter(active=True).first()

    def get_active_assembly_for_member(self, member):
        active_assembly_query = models.Q(
            active=True,
            local_group=None
        ) | models.Q(
            active=True,
            local_group__name=member.local_group
        )
        try:
            assembly = self.get(active_assembly_query)
        except ObjectDoesNotExist as e:
            assembly = None
        finally:
            return assembly

    def get_forthcoming_assembly(self):
        return self.filter(date__gte=timezone.now()).first()


class Assembly(models.Model):
    """
    Assembly definition
    """
    name = models.CharField(
        max_length=150,
        verbose_name=_('Assembly name'),
        help_text=_('Name of the assembly, eg: Asamblea 2020')
    )

    registered = models.ManyToManyField(
        SomUser,
        through='AgRegistration',
        through_fields=('assembly', 'member'),
    )

    date = models.DateField(
        verbose_name=_("Assembly date"),
        help_text=_("Date and hour of this assembly")
    )

    start_votation_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Votation start date"),
        help_text=_("Date and hour when the votation of this assembly starts")
    )

    end_votation_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Votation end date"),
        help_text=_("Date and hour when the votation of this assembly ends")
    )

    active = models.BooleanField(
        verbose_name=('Active'),
        help_text=_('Assembley state')
    )

    local_group = models.ForeignKey(
        LocalGroups,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Local Group'),
        help_text=_('If assembly is for a local group, set blank for '
                    'general assembly'),
        limit_choices_to=models.Q(name__isnull=False)
    )

    assemblies = AssemblyQuerySet.as_manager()

    objects = models.Manager()

    @property
    def is_general_assembly(self):
        return self.local_group is None

    def clean(self):
        if Assembly.assemblies.get_active_assembly() not in (None, self) and self.active:
            raise ValidationError(
                {
                    'active': _('Actually SomCas only supports one active assembly at the same time.')
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __repr__(self):
        return f'<Assembly({self.name})>'

    def __str__(self):
        return self.__repr__()


class AgRegistrationQuerySet(models.QuerySet):

    def member_in_active_virtual_assembly(self, member):
        base_query = models.Q(
            member=member,
            assembly__active=True,
            registration_type=RegistrationChoices.VIRTUAL
        )
        local_group_assembly_query = base_query & models.Q(
            assembly__local_group__name=member.local_group
        )
        general_assembly_query = base_query & models.Q(
            assembly__local_group=None
        )

        return self.filter(
            general_assembly_query | local_group_assembly_query
        ).exists()

    def registration_with_pending_email_confirmation(self, member):
        return self.get(
            member=member,
            assembly__active=True,
            registration_email_sent=False
        )


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

    registrations = AgRegistrationQuerySet.as_manager()

    objects = models.Manager()

    def __repr__(self):
        return f'<AgRegistration({self.assembly.name}, {self.member.username})>'

    def __str__(self):
        return self.__repr__()

# vim: et ts=4 sw=4
