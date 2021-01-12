import pytest
from django.core import mail
from django.utils.translation import gettext as _

from som_cas.models import (
    SomUser,
    AgRegistration,
    RegistrationChoices,
)
from som_cas.utils import send_confirmation_email, locale_override


class TestSomUsers:

    @pytest.mark.django_db
    def test__registered_member_in_active_virtual_assembly(
            self, member_active_agregistry, erp_con
    ):
        user = SomUser.objects.first()

        assert user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test_not_registerd_member_in_active_virtual_assembly(
            self, member_active_agregistry, not_register_member, erp_con
    ):
        user = SomUser.objects.get(username='Alice')

        assert not user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test_not_registered_member_in_active_virtual_assmebly_if_member_in_older_assembly(
            self, active_general_assembly, old_register_in_general_assembly, erp_con
    ):
        user = SomUser.objects.first()

        assert not user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test_not_registered_member_in_active_virtual_assembly_if_inperson_registered_member(
            self, inperson_member_agregistry, erp_con
    ):
        user = SomUser.objects.first()

        assert not user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test_register_member_in_virtual_assembly_if_inperson_registered_member(
            self, inperson_member_agregistry, erp_con
    ):
        user = SomUser.objects.first()
        user_registry = user.register_in_virtual_assembly()

        assert user_registry is None

    @pytest.mark.django_db
    def test_register_member_in_virtual_assembly_if_already_virtual_registered_member(
            self, member_active_agregistry, erp_con
    ):
        user = SomUser.objects.first()
        user_registry = user.register_in_virtual_assembly()

        assert user_registry == member_active_agregistry

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__notRegistered(
            self, active_general_assembly, not_register_member, erp_con
    ):
        member_registry = not_register_member.register_in_virtual_assembly()

        assert member_registry is not None
        assert list(AgRegistration.objects.all()) == [member_registry]
        assert member_registry.member == not_register_member
        assert member_registry.assembly == active_general_assembly
        assert member_registry.registration_type == RegistrationChoices.VIRTUAL

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__olderAssembly(
            self, active_general_assembly, old_register_in_general_assembly,
            not_register_member, erp_con
    ):
        member_registry = not_register_member.register_in_virtual_assembly()

        assert list(AgRegistration.objects.all()) == \
            [old_register_in_general_assembly, member_registry]
        assert member_registry.member == not_register_member
        assert member_registry.assembly == active_general_assembly
        assert member_registry.registration_type == RegistrationChoices.VIRTUAL

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__otherPersonRegistered(
        self, member_active_agregistry, not_register_member, erp_con
    ):
        new_member_registry = not_register_member.register_in_virtual_assembly()
        assert new_member_registry.assembly == member_active_agregistry.assembly
        assert new_member_registry.registration_type == RegistrationChoices.VIRTUAL
        assert list(AgRegistration.objects.all()) == [member_active_agregistry, new_member_registry]

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__noActiveAssembly(
            self, inactive_general_assembly, not_register_member, erp_con
    ):
        member_registry = not_register_member.register_in_virtual_assembly()
        assert member_registry is None
        assert list(AgRegistration.objects.all()) == []

    @pytest.mark.django_db
    def test_register_member_into_localgroup_active_assembly(
            self, active_madridlocalgroup_assembly, not_register_madrid_member,
            erp_con
    ):
        member_registry = not_register_madrid_member.register_in_virtual_assembly()

        assert member_registry.member == not_register_madrid_member
        assert member_registry.assembly == active_madridlocalgroup_assembly
        assert member_registry.registration_type == RegistrationChoices.VIRTUAL

    @pytest.mark.django_db
    def test_register_member_into_other_localgroup_active_assembly(
            self, active_baixmontsenylocalgroup_assembly,
            not_register_madrid_member, erp_con
    ):
        member_registry = not_register_madrid_member.register_in_virtual_assembly()

        assert member_registry is None


class TestConfirmationEmail:

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
        assert email.subject == _('Confirmació d’Inscripció a la Assemblea')
        assert member.first_name in email.body
        with locale_override(member.lang):
            assert assembly.date.strftime('%A').lower() in email.body
            assert str(assembly.date.day) in email.body
            assert assembly.date.strftime('%B').lower() in email.body
            assert _('l\'Assamblea General') in email.body

# vim: noet sw=4 ts=4
