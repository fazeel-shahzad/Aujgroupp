from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'

    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To')
    product_ids = fields.Many2many('product.product')

    def print_report(self):
        data = {}
        data['form'] = self.read(['product_ids', 'date_from', 'date_to'])[0]
        return self.env.ref('sale_report_pdf.action_sale_pdf_report').report_action(self, data=data, config=False)
