# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        values = super(StockMove, self)._prepare_move_line_vals(
            quantity,
            reserved_quant,
        )
        move = self.env['stock.move'].browse(values.get('move_id'))
        if self.env.user.has_group('uom.group_uom'):
            if move.sale_line_id:
                ecoservice_uom_ids = [(0, 0, {
                    'ecoservice_uom_name': uom.ecoservice_uom_name,
                    'ecoservice_uom_type': uom.ecoservice_uom_type,
                    'ecoservice_uom_factor': (uom.ecoservice_uom_factor / uom.order_line_id.product_uom_qty) * quantity,
                }) for uom in move.sale_line_id.ecoservice_uom_ids]
                values.update({'ecoservice_uom_ids': ecoservice_uom_ids})
            else:
                product = self.env['product.product'].browse(
                    values.get('product_id'))
                ecoservice_uom_ids = [(0, 0, {
                    'ecoservice_uom_name': uom.eco_uom_name,
                    'ecoservice_uom_type': uom.eco_uom_type,
                    'ecoservice_uom_factor': uom.eco_factor * quantity,
                }) for uom in product.eco_uom_ids]
                values.update({'ecoservice_uom_ids': ecoservice_uom_ids})
        return values

    def _action_done(self, cancel_backorder=False):
        for move in self:
            for uom in move.mapped('move_line_ids.ecoservice_uom_ids'):
                ml = uom.stock_move_line_id
                uom.ecoservice_uom_factor = (uom.ecoservice_uom_factor / ml.product_qty) * ml.qty_done
        return super(StockMove, self)._action_done(cancel_backorder)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    ecoservice_uom_ids = fields.One2many(
        'ecoservice.order.line.uom', 'stock_move_line_id',
        string='UOMs',
    )
