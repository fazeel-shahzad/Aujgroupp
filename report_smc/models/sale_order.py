from odoo import api, fields, models



class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    discount_percentage = fields.Float('Discount %')
    discount_amount = fields.Float('Discount Amount', compute='compute_discount_amount')
    final_amount = fields.Float('Final Amount')
    section_prod = fields.Many2one('section.product', string="Testing Section")
    def compute_discount_amount(self):
        for val in self:
            val.discount_amount = (val.price_unit*val.product_uom_qty * val.discount) / 100
            val.final_amount = (val.price_unit*val.product_uom_qty- val.discount_amount)

class AddSection(models.Model):
    _name = 'section.product'

    name = fields.Char("Section Name")

class AddSection(models.Model):
    _name = 'section.product'

    name = fields.Char("Section Name")