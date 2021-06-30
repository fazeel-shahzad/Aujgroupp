from odoo import models, fields, api, _


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    is_commission_created = fields.Boolean('Commission is created or not',copy=False)