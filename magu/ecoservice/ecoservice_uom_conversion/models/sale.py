# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full
# copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ecoservice_uom_ids = fields.One2many(
        'ecoservice.order.line.uom', 'order_line_id',
        string='UOMs',
        copy=True,
    )

    def _prepare_invoice_line(self):
        result = super(SaleOrderLine, self)._prepare_invoice_line()
        if self.env.user.has_group('uom.group_uom'):
            result.update({
                'ecoservice_uom_ids': [(6, 0, self.ecoservice_uom_ids.ids)],
            })
        return result

    @api.onchange('product_id', 'product_uom_qty')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.env.user.has_group('uom.group_uom'):
            self.update({'ecoservice_uom_ids': [(5,)]})
            for uom in self.product_id.eco_uom_ids:
                self.update({'ecoservice_uom_ids': [(0, 0, {
                    'ecoservice_uom_name': uom.eco_uom_name,
                    'ecoservice_uom_type': uom.eco_uom_type,
                    'ecoservice_uom_factor': uom.eco_factor * self.product_uom_qty,
                })]})
        return result
