from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AdvancePaymentWizard(models.TransientModel):
    _name = 'advance.payment.wizard'
    _description = 'Advance Payment'

    amount = fields.Float('Advance Amount')
    order_amount = fields.Float('Order Amount')
    user_id = fields.Many2one('res.users')
    branch_id = fields.Many2one('res.branch')
    cheques_payment = fields.Boolean(string="Cheque", default=False)
    online_credit_payment = fields.Boolean(string="Online/ Credit Card", default=False)
    corporate_sale = fields.Boolean(string="Corporate sale", default=False)
    other_receipt = fields.Boolean(string="Other Receipts", default=False)
    is_cash = fields.Boolean(default=False)

    @api.onchange('journal_id')
    def onchange_journal_id(self):
        for rec in self:
            if rec.journal_id.type == 'cash':
                rec.is_cash = True
            else:
                rec.is_cash = False

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
        record = self.env[model].browse(self.env.context.get('active_id'))
        for rec in self:
            vals = {
                'journal_id': rec.journal_id.id,
                'partner_id': record.partner_id.id,
                'date': datetime.today().date(),
                'amount': rec.amount,
                'currency_id': rec.currency_id.id,
                'ref': rec.ref,
                'user_id': rec.user_id.id,
                'branch_id': rec.branch_id.id,
                'cheques_payment': rec.cheques_payment,
                'online_credit_payment': rec.online_credit_payment,
                'corporate_sale': rec.corporate_sale,
                'other_receipt': rec.other_receipt,
                'state': 'draft',
            }
            # if self.journal_id.type == 'cash':
            #     payment = self.env['account.payment'].create(vals)
            #     payment.action_post()
            # elif self.journal_id.type == 'bank':
            #     if self.other_receipt or self.corporate_sale or self.online_credit_payment or self.cheques_payment:
            #         payment = self.env['account.payment'].create(vals)
            #         payment.action_post()
            #     else:
            #         raise UserError('Must Select at least One Option')

            if rec.journal_id.type == 'bank':
                if rec.other_receipt or rec.corporate_sale or rec.online_credit_payment or rec.cheques_payment:
                    payment = self.env['account.payment'].create(vals)
                    payment.action_post()
                else:
                    raise UserError('Must Select at least One Option')
            else:
                payment = self.env['account.payment'].create(vals)
                payment.action_post()

