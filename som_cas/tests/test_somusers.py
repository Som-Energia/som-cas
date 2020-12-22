import pytest
from django.core import mail

from som_cas.models import (
    SomUser,
    AgRegistration,
    RegistrationChoices,
)
from som_cas.utils import send_confirmation_email

class TestSomUsers:

    @pytest.mark.django_db
    def test__registered_member_in_active_virtual_assembly(
            self, member_registry, erp_con
    ):
        user = SomUser.objects.first()

        assert user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test_not_registerd_member_in_active_virtual_assembly(
            self, member_registry, not_register_member, erp_con
    ):
        user = SomUser.objects.get(username='Alice')

        assert not user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test__isVirtualRegisteredInActiveAssembly__inOlderAssembly(
            self, member_inactive_registry, erp_con
    ):
        user = SomUser.objects.first()

        assert not user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test__isVirtualRegisteredInActiveAssembly__inPerson(
            self, inperson_member_registry, erp_con
    ):
        user = SomUser.objects.first()

        assert not user.is_registered_in_active_virtual_assembly()

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__inPerson(
            self, inperson_member_registry, erp_con
    ):
        user = SomUser.objects.first()
        user_registry = user.register_in_virtual_assembly()

        assert user_registry is None

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__virtual(
            self, member_registry, erp_con
    ):
        user = SomUser.objects.first()
        user_registry = user.register_in_virtual_assembly()

        assert user_registry == member_registry

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
        assert member_registry.member, not_register_member
        assert member_registry.assembly, active_general_assembly
        assert member_registry.registration_type == RegistrationChoices.VIRTUAL

    @pytest.mark.django_db
    def test__registerInVirtualAssembly__otherPersonRegistered(
        self, member_registry, not_register_member, erp_con
    ):
        new_member_registry = not_register_member.register_in_virtual_assembly()
        assert new_member_registry.assembly == member_registry.assembly
        assert new_member_registry.registration_type == RegistrationChoices.VIRTUAL
        assert list(AgRegistration.objects.all()) == [member_registry, new_member_registry]

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
    def test_send_confirmation_email(
        self, pending_email_member_registry
    ):
        email_template = 'som_cas/mail_confirmation.html'
        member = pending_email_member_registry.member
        send_confirmation_email(member, email_template)

        assert len(mail.outbox) == 1

# vim: noet sw=4 ts=4