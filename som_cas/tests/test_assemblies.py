from datetime import datetime

import pytest
from django.core.exceptions import ValidationError

from som_cas.models import Assembly, LocalGroups


class TestAssembly:

    @pytest.mark.django_db
    def test_cannot_create_two_actived_assamblies(
            self, active_general_assembly, local_group
    ):
        with pytest.raises(ValidationError) as e:
            new_assembly = Assembly(
                name='Awesome Assembley',
                date=datetime.now(),
                active=True,
                local_group=LocalGroups.objects.first()
            )
            new_assembly.save()

        assert 'only supports one active assembly' in str(e.value)
