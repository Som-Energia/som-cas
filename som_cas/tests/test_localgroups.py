from unittest import mock

import pytest


class TestLocalGroups:

    @pytest.mark.django_db
    def test_identifyLocalGroup_matchingByCity(self, user, local_group):
        with mock.patch(
                'som_cas.models.SomUser.address_codes',
                new_callable=mock.PropertyMock
        ) as mock_address_codes:
            mock_address_codes.return_value = ('09', '08', '08039')

            assert user.local_group == 'BaixMontseny'

    @pytest.mark.django_db
    def test_identifyLocalGroup_notMatchingByCity(self, user, local_group):
        with mock.patch(
                'som_cas.models.SomUser.address_codes',
                new_callable=mock.PropertyMock
        ) as mock_address_codes:
            mock_address_codes.return_value = ('09', '08', '08038')

            assert user.local_group == ''

    @pytest.mark.django_db
    def test_identifyLocalGroup_matchingByState(self, user, local_group):
        with mock.patch(
                'som_cas.models.SomUser.address_codes',
                new_callable=mock.PropertyMock
        ) as mock_address_codes:
            mock_address_codes.return_value = ('09', '04', '04008')

            assert user.local_group == 'Almeria'

    @pytest.mark.django_db
    def test_identifyLocalGroup_matchingByCCAA(self, user, local_group):
        with mock.patch(
                'som_cas.models.SomUser.address_codes',
                new_callable=mock.PropertyMock
        ) as mock_address_codes:
            mock_address_codes.return_value = ('13', '28', '28791')

            assert user.local_group == 'Comunidad de Madrid'

    @pytest.mark.django_db
    def test_identifyLocalGroup_matchingByState_Girona(self, user, local_group):
        with mock.patch(
                'som_cas.models.SomUser.address_codes',
                new_callable=mock.PropertyMock
        ) as mock_address_codes:
            mock_address_codes.return_value = ('09', '17', '17142')

            assert user.local_group == 'Girona'