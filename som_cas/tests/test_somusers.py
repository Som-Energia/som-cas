import pytest

from som_cas.models import (
    SomUser,
    AgRegistration,
    RegistrationChoices,
)


class TestSomUsers():

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
        assert member_registry.registration_type, RegistrationChoices.VIRTUAL

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


# vim: noet sw=4 ts=4
