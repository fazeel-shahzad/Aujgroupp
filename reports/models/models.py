from odoo import models, fields, api


class InheritDelivery(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def action_open_delivery_wizard(self):

        data = {
            'model': 'choose.delivery.carrier',
            'display_price': self.display_price,
            'carrier_id': self.carrier_id,
        }
        print("Data", data)
        return self.env.ref('reports.report_dic_img_id').with_context().report_action(self, data=data)