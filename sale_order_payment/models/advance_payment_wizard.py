from datetime import datetime

from odoo import models, fields


class AdvancePaymentWizard(models.TransientModel):
    _name = 'advance.payment.wizard'
    _description = 'Advance Payment'

    amount = fields.Float('Advance Amount')
    order_amount = fields.Float('Order Amount')
    user_id = fields.Many2one('res.users')
    branch_id = fields.Many2one('res.branch')
    wiz_date= fields.Date('Date')
    wiz_description = fields.Text('Description')
    cheque_no = fields.Char(string ="Cheque no")
    paid_by = fields.Char(string= "Paid by")
    received_by = fields.Char(string= "Received by")
    approved_by = fields.Char(string= "Paid by")

    def default_payment_method_id(self):
        method = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
        return method.id

    def default_journal_id(self):
        journal = self.env['account.journal'].search([('name', '=', 'Cash')])
        return journal.id

    journal_id = fields.Many2one('account.journal', default=default_journal_id)
    payment_method_id = fields.Many2one('account.payment.method', default=default_payment_method_id)
    ref = fields.Char('Reference')

    def default_currency_id(self):
        currency = self.env['res.currency'].search([('name', '=', 'PKR')])
        return currency.id

    currency_id = fields.Many2one('res.currency', default=default_currency_id)

    def create_data(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        vals = {
            'journal_id': self.journal_id.id,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'partner_type': 'customer',
            'partner_id': rec.partner_id.id,
            'payment_date':self.wiz_date,
            'amount': self.amount,
            'currency_id': rec.currency_id.id,
            'communication': self.ref,
            'so_number': self.ref,
            'user_id': self.user_id.id,
            'payment_type': 'inbound',
            'state': 'draft',
            'wiz_description':self.wiz_description,
            'cheque_no':self.cheque_no,
            'paid_by':self.paid_by,
            'received_by':self.received_by,
            'approved_by':self.approved_by
        }
        payment = self.env['account.payment'].create(vals)
        payment.post()

