# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    is_sale_taxes_added = fields.Boolean('Sales Taxes Added?')

    def action_apply_taxes(self):
        tax = self.env['account.tax'].search([('name', '=', 'Sales Tax')])
        if tax:
            for line in self.order_line:
                if line.product_id.type != 'service':
                    line.tax_id = [tax.id]
        self.is_sale_taxes_added = True

    def action_remove_taxes(self):
        for line in self.order_line:
            line.tax_id = None
        self.is_sale_taxes_added = False



