# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


class PaymentWizardInherit(models.TransientModel):
    _inherit = "account.payment.register"

    cheques_payment = fields.Boolean(string="Cheque", default=False)
    online_credit_payment = fields.Boolean(string="Online/ Credit Card", default=False)
    corporate_sale = fields.Boolean(string="Corporate sale", default=False)
    other_receipt = fields.Boolean(string="Other Receipts", default=False)
    branch_id = fields.Many2one('res.branch', default=lambda r: r.env.user.branch_id.id)
    type = fields.Selection(related='journal_id.type')

    @api.onchange('branch_id')
    def onchange_get_branches(self):
        branches = self.env.user.branch_ids
        return {'domain': {'branch_id': [('id', 'in', branches.ids)]}}

    def _create_payments(self):
        if self.journal_id.type == 'bank':
            if self.cheques_payment == False and self.online_credit_payment == False and self.corporate_sale == False and self.other_receipt == False:
                raise UserError(_("Must select one option out of 4"))
        res = super(PaymentWizardInherit, self)._create_payments()

        if self.cheques_payment == True:
            res.update({'cheques_payment': True})

        if self.online_credit_payment == True:
            res.update({'online_credit_payment': True})

        if self.corporate_sale == True:
            res.update({'corporate_sale': True})

        if self.other_receipt == True:
            res.update({'other_receipt': True})
        if self.branch_id:
            res.update({'branch_id': self.branch_id.id})

        return res

    @api.onchange('cheques_payment')
    def cheque_only(self):
        if self.cheques_payment:
            if self.journal_id.type == 'cash':
                self.online_credit_payment = False
            if self.journal_id.type == 'bank':
                self.other_receipt = False
                self.corporate_sale = False
                self.online_credit_payment = False

    @api.onchange('online_credit_payment')
    def creditCard_only(self):
        if self.online_credit_payment:
            if self.journal_id.type == 'cash':
                self.cheques_payment = False
            if self.journal_id.type == 'bank':
                self.other_receipt = False
                self.cheques_payment = False
                self.corporate_sale = False

    @api.onchange('corporate_sale')
    def corporate_only(self):
        if self.corporate_sale:
            if self.journal_id.type == 'cash':
                self.other_receipt = False
            if self.journal_id.type == 'bank':
                self.other_receipt = False
                self.cheques_payment = False
                self.online_credit_payment = False

    @api.onchange('other_receipt')
    def otherReceipt_only(self):
        if self.other_receipt:
            if self.journal_id.type == 'cash':
                self.corporate_sale = False
            if self.journal_id.type == 'bank':
                self.corporate_sale = False
                self.cheques_payment = False
                self.online_credit_payment = False


class BranchReport(models.TransientModel):
    _name = 'branch.wizard'
    _description = 'Branch Report'

    date_from = fields.Date(string='Date From', required=True, default=datetime.today())
    date_to = fields.Date(string='Date To', required=True, default=datetime.today())
    branch = fields.Many2one('res.branch', string="Branch", required=True)

    @api.constrains('date_to', 'date_from')
    def date_constrains(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    def print_pdf_action(self):
        data = {
            'model': 'branch.wizard',
            'ids': self.ids,
            'form': {
                'date_from': self.date_from, 'date_to': self.date_to, 'branch': self.branch,
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('branch_report.report_branch_id').report_action(self, data=data)

    # branch = fields.Many2one('res.branch', string="Branch")
    # date_from = fields.Date("Date From")
    # date_to = fields.Date("Date To")
    #
    # def print_pdf_action(self):
    #     print('kkkk', self.read()[0])
    #
    #     data = {
    #         'model': 'branch.wizard',
    #         'form': self.read()[0]
    #     }
    #     selected_id = data['form']['branch'][0]
    #     date_from = data['form']['date_from']
    #     date_to = data['form']['date_to']
    #
    #     @api.multi
    #     def get_report(self):
    #         data = {
    #             'model': self._name,
    #             'ids': self.ids,
    #             'form': {
    #                 'date_start': self.date_start, 'date_end': self.date_end,
    #             },
    #         }
    #
    #         # line = self.SaleOrderLine.search([('order_id', '=', self.sale_normal_delivery_charges.id),
    #         total_values = self.env['account.payment'].search([('branch_id.id', '=', selected_id)])
    #
    #     return self.env.ref('branch_report.report_branch_id').report_action(self, data=data)


class InheritAccountPayment(models.Model):
    _inherit = 'account.payment'
