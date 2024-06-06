from urllib.parse import urlparse

import pytest
from django.http.request import QueryDict
from django.urls import reverse
from django.utils.translation import gettext as _


class TestSomCasLoginView:
    BASE_URL = reverse('cas_login')

    @pytest.mark.django_db
    def test_participa_login_view(self, client):
        service = 'https://participa.somenergia.coop'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        assert 'doctype' in res.content.decode()

    @pytest.mark.django_db(databases=['default', 'users_db'])
    def test_participa_login_post(self, client, members_db):
        service = 'https://participa.somenergia.coop'
        url = f'{self.BASE_URL}?service={service}'
        res = client.post(
            url,
            {'username': 'Alice', 'password': '1234'},
        )

        response_url = urlparse(res.url)
        response_query = QueryDict(response_url.query)
        assert res.status_code == 302
        assert f'{response_url.scheme}://{response_url.netloc}' == service
        assert 'ticket' in response_query
        assert response_query.get('ticket', None) is not None

    @pytest.mark.django_db(databases=['default', 'users_db'])
    def test_participa_login_post_bad_password(self, client, members_db):
        service = 'https://participa.somenergia.coop'
        url = f'{self.BASE_URL}?service={service}'
        res = client.post(
            url,
            {'username': 'Alice', 'password': '12asd34'},
        )

        assert res.status_code == 200
        assert not res.context['form'].is_valid()
        assert _('The username or password is not correct') in res.content.decode()

    @pytest.mark.django_db
    def test_active_forthcoming_general_assembly_login_view(
        self, client, active_forthcoming_assembly
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
        service = 'https://aulapopular.somenergia.coop/'

        res = client.get(self.BASE_URL, {'service': service})

        assert res.status_code == 200
        content = res.content.decode()
        assert 'Logotip_aula_popular.png' in content
        assert '<span class="login100-form-title-text m-b-32 m-t-32"></span>' in content
