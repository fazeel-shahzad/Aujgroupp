# from pandas.tests.extension import arrow

from odoo import models, fields, api
from datetime import datetime


class RateComparison(models.TransientModel):
    _name = 'rate.report'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    # vendor_id = fields.Many2many("res.partner", string="Vendor", default=lambda self: self.env['res.partner'].search([('supplier_rank','=',1)]))
    vendor_id = fields.Many2many("res.partner", string="Vendor")

    # month_range = fields.Char(compute="compute_month_range")
    #
    # @api.onchange('vendor_id')
    # def compute_month_range(self):
    #     for d in arrow.Arrow.range('month', self.date_from, self.date_to):
    #         print(d.month, d.format('MMMM'))

    def create_wizard_rate(self):
        data = {}
        data['form'] = self.read()[0]
        return self.env.ref('rate_comparison_report.rate_comparison_rep').report_action(self,data=data, config=False)

    def _get_report_values(self, docids, data=None):
        return {
            'data': data,
            'doc_ids': docids,
        }
