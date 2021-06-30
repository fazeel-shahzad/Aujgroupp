from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_dz_customer = fields.Boolean("Is Daraz Customer?")


    # def create_or_update_dz_customer(self, vals, is_company=False, parent_id=False, type=False,
    #                                  dz_instance=False):
    #     country_obj = self.env['res.country']
    #     state_obj = self.env['res.country.state']

    #     first_name = vals.get('CustomerFirstName')
    #     last_name = vals.get('CustomerLastName')

    #     if not first_name and not last_name :
    #         return False
    #     name = "%s %s" % (first_name, last_name)

    #     bill_address = vals.get('AddressBilling')
    #     bill_first_name = bill_address.get('CustomerFirstName')
    #     bill_last_name = bill_address.get('CustomerLastName')
    #     phone = bill_address.get("Phone")
    #     phone = bill_address.get("Phone2")
    #     address1 = bill_address.get('Address1')
    #     address2 = bill_address.get('Address2')
    #     address3 = bill_address.get('Address3')
    #     address4 = bill_address.get('Address4')
    #     address5 = bill_address.get('Address5')
    #     email = bill_address.get('CustomerEmail')
    #     city = bill_address.get('City')
    #     zip = bill_address.get('PostCode')
    #     country_name = bill_address.get('Country')
    #     # state_name = bill_address.get('state')

    #     country = country_obj.search([('code', '=', country_name)], limit=1)

    #     partner = False
    #     partner = email and self.search(
    #             ['|', ('email', '=', email), ('phone', '=', phone), ('is_company', '=', False)], limit=1) or False
    #     if not partner and type:
    #         partner = self.search(
    #             [('name', '=', name), ('city', '=', city), ('street', '=', address1), ('street2', '=', address2),
    #              ('zip', '=', zip), ('country_id', '=', country.id)], limit=1)
    #     if partner and not type:
    #         partner.with_context(res_partner_search_mode='customer').write(
    #             {'is_company': False,
    #              'phone': phone or partner.phone,
    #              'is_dz_customer': True,
    #              'email': email or False})
    #     elif not partner:
    #         partner = self.with_context(res_partner_search_mode='customer').create(
    #             {'type': type, 'parent_id': parent_id, 'is_dz_customer': True,
    #              'name': name,  'city': city,
    #              'street': address1, 'street2': address2,
    #              'phone': phone, 'zip': zip, 'email': email,
    #              'country_id': country and country.id or False, 'is_company': False,
    #              })
    #     return partner

    # @api.model
    # def import_wc_customers(self, dz_instance=False):
    #     if not dz_instance:
    #         return False
    #
    #     for customer in wc_customers:
    #         partner = False
    #         billing_addr = customer.get('billing', False)
    #         shipping_addr = customer.get('shipping', False)
    #         company_id = False
    #         if billing_addr:
    #             if billing_addr.get('company'):
    #                 company_id = self.create_or_update_wc_customer(billing_addr, True, False, False,
    #                                                                dz_instance)
    #             partner = self.create_or_update_wc_customer(billing_addr, False,
    #                                                         company_id and company_id.id or False, False,
    #                                                         dz_instance)
    #         if partner and shipping_addr:
    #             self.create_or_update_wc_customer(shipping_addr, False, company_id and company_id or partner.id,
    #                                               'delivery',
    #                                               dz_instance)
