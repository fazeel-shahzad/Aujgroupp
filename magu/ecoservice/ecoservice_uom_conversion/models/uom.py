# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full
# copyright and licensing details.

from odoo import fields, models


class UoMCategory(models.Model):
    _inherit = 'uom.category'

    uom_template = fields.Boolean(
        string='UOM Template',
    )

    _sql_constraints = [
        ('uom_category_unique_type', 'Check(1=1)',
         'You can have only one category per measurement type.'),
    ]


class EcoserviceUOM(models.Model):
    _name = 'ecoservice.uom'
    _description = 'Ecoservice Unit of measure'

    eco_product_template_id = fields.Many2one('product.template')
    eco_product_id = fields.Many2one('product.product')
    eco_uom_id = fields.Many2one('uom.uom')
    eco_uom_name = fields.Char(
        string='Unit of Measure',
        readonly=False,
    )
    eco_factor = fields.Float(
        string='Ratio',
        default=1.0,
        digits=(12, 5),
        readonly=False,
    )
    eco_uom_type = fields.Selection([
        ('bigger', 'Bigger than the reference Unit of Measure'),
        ('reference', 'Reference Unit of Measure for this category'),
        ('smaller', 'Smaller than the reference Unit of Measure')],
        string='Type',
        readonly=False,
        required=True,
    )
    eco_category_id = fields.Many2one(
        'uom.category',
        domain=lambda self: [('uom_template', '=', True)],
        string='Category',
        required=False,
    )


class EcoserviceOrderLineUOM(models.Model):
    _name = 'ecoservice.order.line.uom'
    _description = 'Ecoservice Unit of measure for Order Lines'

    ecoservice_product_id = fields.Many2one('product.product')
    ecoservice_product_template_id = fields.Many2one('product.template')
    order_line_id = fields.Many2one('sale.order.line')
    stock_move_line_id = fields.Many2one('stock.move.line')
    account_move_line_id = fields.Many2one('account.move.line')
    ecoservice_uom_name = fields.Char(
        string='Unit of Measure',
    )
    ecoservice_uom_factor = fields.Float(
        string='Ratio',
        default=1.0,
        digits=(12, 5),
    )
    ecoservice_uom_type = fields.Selection([
        ('bigger', 'Bigger than the reference Unit of Measure'),
        ('reference', 'Reference Unit of Measure for this category'),
        ('smaller', 'Smaller than the reference Unit of Measure')],
        string='Type',
        required=True,
    )
    ecoservice_uom_category_id = fields.Many2one(
        'uom.category',
        domain=lambda self: [('uom_template', '=', True)],
        string='Category',
        required=False,
    )
