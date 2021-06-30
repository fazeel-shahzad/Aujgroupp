# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BrachReport(models.Model):
    _inherit = 'account.payment'

    # def branch_report_action(self):
    #     pass
    five_th = fields.Integer(string="5000 x")
    one_th = fields.Integer(string="1000 x")
    five_hundred = fields.Integer(string='500 x')
    currency_note = fields.Boolean(string="Note", default=False)
    cheques_payment = fields.Boolean(string="Cheque", default=False)
    online_credit_payment = fields.Boolean(string="Online/ Credit Card", default=False)
    corporate_sale = fields.Boolean(string="Corporate sale", default=False)
    other_receipt = fields.Boolean(string="Other Receipts", default=False)
    type = fields.Selection(related='journal_id.type')

    @api.model
    def create(self, vals):
        if vals['other_receipt'] or vals['corporate_sale'] or vals['online_credit_payment'] or vals['cheques_payment']:
            return super(BrachReport, self).create(vals)
        else:
            raise UserError('Must Select at least One Option')

    @api.onchange('cheques_payment')
    def onchange_cheque_only(self):
        if self.cheques_payment:
            if self.journal_id.type == 'cash':
                self.online_credit_payment = False
            if self.journal_id.type == 'bank':
                self.other_receipt = False
                self.corporate_sale = False
                self.online_credit_payment = False

    @api.onchange('online_credit_payment')
    def onchange_creditCard_only(self):
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

    @api.onchange('partner_id')
    def curr_note_check(self):
        if self.partner_id:
            if self.partner_id.ceo_currency_check == True:
                self.currency_note = True
            elif self.partner_id.ceo_currency_check == False:
                self.currency_note = False

    @api.onchange('cheques_payment')
    def cheque_only(self):
        if self.cheques_payment:
            self.online_credit_payment = False

    @api.onchange('online_credit_payment')
    def creditCard_only(self):
        if self.online_credit_payment:
            self.cheques_payment = False

    def action_post(self):

        amnt_in_note = (5000 * self.five_th) + (1000 * self.one_th) + (500 * self.five_hundred)

        if self.partner_id.ceo_currency_check == True:
            if self.amount == amnt_in_note:
                res = super(BrachReport, self).action_post()
                return res
            else:
                raise UserError(_('Amount is not equal to Currency note.'))
        else:
            res = super(BrachReport, self).action_post()
            return res


class resPartner_CurrencyNote(models.Model):
    _inherit = "res.partner"

    ceo_currency_check = fields.Boolean(string="Currency Note", default=False)
