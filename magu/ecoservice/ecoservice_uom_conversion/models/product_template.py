# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_categ_id = fields.Many2one(
        'uom.category',
        domain=lambda self: [('uom_template', '=', True)],
        string='UOM Category',
        compute='_compute_uom_category',
        inverse='_inverse_uom_category',
        store=True,
    )
    eco_uom_ids = fields.One2many(
        'ecoservice.uom', 'eco_product_template_id',
        string='UOM Template',
    )

    @api.depends('product_variant_ids', 'product_variant_ids.uom_categ_id')
    def _compute_uom_category(self):
        context = self._context
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            if context.get('create_product_product'):
                template.write({'uom_categ_id': template.product_variant_ids.uom_categ_id.id,
                                'eco_uom_ids': [(6, 0, template.product_variant_ids.eco_uom_ids.ids)]})
        if not unique_variants:
            self.uom_categ_id = False
            self.eco_uom_ids = [(5,)]

    def _inverse_uom_category(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.uom_categ_id = template.uom_categ_id

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

    @api.model
    def create(self, vals):
        template = super(ProductTemplate, self).create(vals)
        if len(template.product_variant_ids) == 1:
            template.product_variant_ids.write({
                'uom_categ_id': template.uom_categ_id.id,
                'eco_uom_ids': [(6, 0, template.eco_uom_ids.ids)],
            })
        return template

    def write(self, vals):
        template = super(ProductTemplate, self).write(vals)
        for tmpl in self:
            if len(tmpl.product_variant_ids) == 1:
                tmpl.product_variant_ids.uom_categ_id = tmpl.uom_categ_id.id
                tmpl.product_variant_ids.eco_uom_ids = [
                    (6, 0, tmpl.eco_uom_ids.ids)]
        return template
