from odoo import models, fields, api
from odoo.exceptions import Warning


class CancelReason(models.TransientModel):
    _name = 'cancel.reason'
    _description = "Cancel Reason"

    cancel_reason = fields.Selection([('delay', 'Sourcing Delay(cannot meet deadline)'),
                                     ('out_of_stock', 'Out of Stock'), 
                                     ('wrong_price', 'Wrong Price or Pricing Error')
                                    ], string="Cancel Reason", copy=False)
    order_id = fields.Many2one('sale.order', string='Sale Order')

    def process(self):
        self.order_id.cancel_reason = self.cancel_reason
        return self.order_id.daraz_order_cancel(flag=True)