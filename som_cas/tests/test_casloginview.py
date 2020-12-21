import pytest
from django.urls import reverse
from django.utils.translation import gettext as _

from som_cas.views import SomCasLoginView

class TestSomCasLoginView:

    BASE_URL = reverse('cas_login')

    @pytest.mark.django_db
    def test_participa_login_view(self, client):
        service = 'https://participa.somenergia.coop'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        assert _('Engage!') in res.content.decode()

    @pytest.mark.django_db
    def test_active_general_assembly_login_view(
            self, client, active_general_assembly
    ):
        service = 'https://agvirtual.somenergia.coop'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        content = res.content.decode()
        assert 'logo-somenergia-transparent.png' in content

        assert _('Assemblea General') in content

    @pytest.mark.django_db
    def test_inactive_general_assembly_login_view(
            self, client, inactive_general_assembly
    ):
        service = 'https://agvirtual.somenergia.coop'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        content = res.content.decode()
        assert 'logo-somenergia-transparent.png' in content
        assert 'alert alert-danger' in content
        assert 'No active assembly' in content

    @pytest.mark.django_db
    def test_local_assembly_login_view(
        self, client, active_madridlocalgroup_assembly
    ):
        service = 'https://agvirtual.somenergia.coop'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        content = res.content.decode()
        assert 'logo-somenergia-transparent.png' in content
        assert 'Madrid' in content

    @pytest.mark.django_db
    def test_accademy_login_view(self, client):
        service = 'https://formacio.somenergia.coop'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        content = res.content.decode()
        assert 'Logotip_aula_popular.png' in content
        assert '<span class="login100-form-title-text m-b-32 m-t-32"></span>' in content
