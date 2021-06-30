from odoo import models, fields, api,_
from odoo.exceptions import UserError
from datetime import datetime
from datetime import date, timedelta

class SOTeamwiseReportWizard(models.TransientModel):
    _name = 'so.teamwise.report.wizard'
    _description = 'sales persons wise report'



    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    saleperson_ids = fields.Many2many('res.users', default=lambda self: self.env['res.users'].search([]))




    def print_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self.env.ref('so_teamwise_report.action_so_teamwise_pdf_report').report_action(self, data=data, config=False)