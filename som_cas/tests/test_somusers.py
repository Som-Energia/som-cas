import pytest

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
    def test__virtual_register_in_general_assembly__not_registered(
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


# vim: noet sw=4 ts=4
