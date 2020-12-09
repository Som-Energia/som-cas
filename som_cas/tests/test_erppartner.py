from som_cas.contrib import ERPPartner
from . import factories


class TestERPPartner:

    def test_memberAddressCodes(self, erp_con):
        erp_partner = ERPPartner(factories.personaldata.vat)

        assert erp_partner.address_codes == ('09', '08', '08217')

    def test_memberNotExists(self, erp_con):
        erp_partner = ERPPartner(factories.personaldata.badvat)

        assert erp_partner.address_codes == ()
