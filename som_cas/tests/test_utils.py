import pytest
from django.core import mail
from django.utils.translation import gettext as _

from som_cas.utils import is_assembly_service, send_confirmation_email, locale_override


class TestUtils:

    def test_is_assembly_service(self, erp_con):
        service = 'https://agvirtual.somenergia.coop'

        assert is_assembly_service(service)

    def test_is_assembly_service_empty_service(self, erp_con):

        assert not is_assembly_service('')

    @pytest.mark.django_db
    def test_send_confirmation_email_general_assembly(
        self, pending_email_member_registry
    ):
        email_template = 'som_cas/mail_confirmation.html'
        member = pending_email_member_registry.member
        assembly = pending_email_member_registry.assembly

        send_confirmation_email(member, email_template)

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert member.email in email.to
        assert email.subject == _('Confirmació d’inscripció a la Assemblea')
        assert member.first_name in email.body
        with locale_override(member.lang):
            assert assembly.date.strftime('%A').lower() in email.body
            assert str(assembly.date.day) in email.body
            assert assembly.date.strftime('%B').lower() in email.body
            assert _('l\'Assamblea General') in email.body
    
    @pytest.mark.django_db
    def test_send_confirmation_email_localgroup_assembly(
        self, pending_email_member_registry_localgroup_assembly
    ):
        email_template = 'som_cas/mail_confirmation.html'
        member = pending_email_member_registry_localgroup_assembly.member
        assembly = pending_email_member_registry_localgroup_assembly.assembly

        send_confirmation_email(member, email_template)

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert member.email in email.to
        assert email.subject == _("Confirmació d'inscripció {}".format(assembly.local_group.alias))
        assert member.first_name in email.body
        with locale_override(member.lang):
            assert assembly.date.strftime('%A').lower() in email.body
            assert str(assembly.date.day) in email.body
            assert assembly.date.strftime('%B').lower() in email.body
            assert assembly.local_group.full_name in email.body
            assert assembly.local_group.email in email.body
            assert assembly.local_group.logo.url in email.body
