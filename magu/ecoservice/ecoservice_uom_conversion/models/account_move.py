# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    ecoservice_uom_ids = fields.One2many(
        'ecoservice.order.line.uom', 'account_move_line_id',
        string='UOMs',
        copy=True,
    )

    @api.onchange('product_id', 'quantity')
    def _onchange_product_qty(self):
        if self.env.user.has_group('uom.group_uom'):
            self.update({'ecoservice_uom_ids': [(5,)]})
            for uom in self.product_id.eco_uom_ids:
                self.update({'ecoservice_uom_ids': [(0, 0, {
                    'ecoservice_uom_name': uom.eco_uom_name,
                    'ecoservice_uom_type': uom.eco_uom_type,
                    'ecoservice_uom_factor': uom.eco_factor * self.quantity,
                })]})
