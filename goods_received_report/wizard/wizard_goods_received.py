from odoo import models, fields, api,_
from odoo.exceptions import UserError
from datetime import datetime
from datetime import date, timedelta

class POGoodsReceivedReportWizard(models.TransientModel):
    _name = 'po.goods.report.wizard'
    _description = 'Purchase order goods received report'

    date_from = fields.Datetime('Date From')
    date_to = fields.Datetime('Date To')
    # product_ids = fields.Many2many('product.product')

    def print_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self.env.ref('goods_received_report.action_po_goods_pdf_report').report_action(self, data=data, config=False)