import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from som_cas.models import Assembly, LocalGroups


class TestAssembly:

    @pytest.mark.django_db
    def test_cannot_create_two_actived_assamblies(
            self, active_general_assembly, local_group
    ):
        with pytest.raises(ValidationError) as e:
            new_assembly = Assembly(
                name='Awesome Assembley',
                date=timezone.now(),
                active=True,
                local_group=LocalGroups.objects.first()
            )
            new_assembly.save()

        assert 'only supports one active assembly' in str(e.value)

    @pytest.mark.django_db
    def test_get_inactive_forthcoming_assembly(
            self, inactive_forthcoming_assembly
    ):
        # given a inactive forthcoming assembly
        # forthcoming_assembly

        # when we search for the forthcoming assembly
        assembly = Assembly.assemblies.get_forthcoming_assembly()

        # then that assembly is not None
        assert assembly is not None
        # and is not active
        assert not assembly.active

    @pytest.mark.django_db
    def test_get_active_forthcoming_assembly__with_more_assemblies(
            self, assemblies_with_active_forthcoming_assembly
    ):
        # given a set of assemblies with a forthcoming assembly
        # assemblies_with_active_forthcoming_assembly

        # when we search for the forthcoming assembly
        assembly = Assembly.assemblies.get_forthcoming_assembly()

        # then that assembly is not None
        assert assembly is not None
        # and is active
        assert assembly.active
