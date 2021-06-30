# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    uom_categ_id = fields.Many2one(
        'uom.category',
        domain=lambda self: [('uom_template', '=', True)],
        string='UOM Category',
    )
    eco_uom_ids = fields.One2many(
        'ecoservice.uom', 'eco_product_id',
        string='UOM Product',
    )

    @api.onchange('uom_categ_id')
    def onchange_uom_categ_id(self):
        self.update({'eco_uom_ids': [(5,)]})
        uom_ids = self.env['uom.uom'].search(
            [
                ('category_id', '=', self.uom_categ_id.id),
            ],
            order='id',
        )
        for uom in uom_ids:
            if uom.uom_type == 'bigger':
                ratio = uom.factor_inv
            elif uom.uom_type in ['smaller', 'reference']:
                ratio = uom.factor
            self.update({'eco_uom_ids': [(0, 0, {
                'eco_uom_name': uom.name,
                'eco_uom_type': uom.uom_type,
                'eco_factor': ratio,
            })]})
