from .middleware import get_erp_con


class ERPPartner:

    ATTRIBUTES = [
        'id'
    ]

    def __init__(self, vat):
        self.erp_con = get_erp_con()
        self.Partner = self.erp_con.model('res.partner')
        partner_id = self.Partner.search([('vat', '=', "ES" + vat)])
        if partner_id:
            for attr, value in self.Partner.read(partner_id[0], self.ATTRIBUTES).items():
                setattr(self, attr, value)

    @property
    def address_codes(self):
        if hasattr(self, 'id'):
            city_id = self.Partner.read(
                self.id, ['www_municipi']
            )['www_municipi'][0]
            city = self.erp_con.ResMunicipi.read(city_id, ['ine', 'state'])
            city_code = city['ine']
            state_id = city['state'][0]
            state = self.erp_con.ResCountryState.read(
                state_id, ['code', 'comunitat_autonoma']
            )
            state_code = state['code']
            ccaa_id = state['comunitat_autonoma'][0]
            ccaa = self.erp_con.ResComunitat_autonoma.read(ccaa_id, ['codi'])
            ccaa_code = ccaa['codi']
            return (ccaa_code, state_code, city_code)
        return ()
