from som_cas.utils import is_assembly_service


class TestUtils:

    def test_is_assembly_service(self, erp_con):
        service = 'https://agvirtual.somenergia.coop'

        assert is_assembly_service(service)

    def test_is_assembly_service_empty_service(self, erp_con):

        assert not is_assembly_service('')
