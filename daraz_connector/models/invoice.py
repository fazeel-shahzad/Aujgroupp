from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.move"

    global_daraz_rate = fields.Float('Global Daraz Fee')
    daraz_fee = fields.Monetary(string='Daraz Fee', compute='_compute_amount',
                                         store=True, track_visibility='always')
    fees_account_id = fields.Integer(compute='verify_discount')
    instance_id = fields.Many2one('daraz.connector', 'Daraz Store')

    @api.depends('company_id')
    def verify_discount(self):
        for rec in self:
            rec.fees_account_id = rec.instance_id.fees_account_id.id

    # 1. tax_line_ids is replaced with tax_line_id. 2. api.mulit is also removed.
    @api.depends('line_ids.debit','line_ids.credit','line_ids.currency_id',
        'line_ids.amount_currency', 'line_ids.amount_residual','line_ids.amount_residual_currency',
        'line_ids.payment_id.state','global_daraz_rate')
    def _compute_amount(self):
        res = super(AccountInvoice, self)._compute_amount()
        for rec in self:
            if not ('global_tax_rate' in rec) :# and rec.daraz_fee:
                rec.calculate_discount()
            sign = rec.type in ['in_refund', 'out_refund'] and -1 or 1
            rec.amount_total_company_signed = rec.amount_total * sign
            rec.amount_total_signed = rec.amount_total * sign

        return res

    def calculate_discount(self):
        for rec in self:
            rec.daraz_fee = rec.global_daraz_rate if rec.amount_untaxed > 0 else 0            
            rec.amount_total = rec.amount_tax + rec.amount_untaxed + rec.daraz_fee
            rec.amount_residual = rec.amount_total
            rec.update_universal_discount()

    def update_universal_discount(self):
        """This Function Updates the Add or subtract fees through daraz transaction"""
        for rec in self:
            already_exists = self.line_ids.filtered(lambda line: line.name and line.name.find('Daraz Fees') == 0)
            terms_lines = self.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
            other_lines = self.line_ids.filtered(
                lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
            if already_exists:
                amount = rec.daraz_fee
                currency_id = rec.currency_id
                amount = currency_id._convert(amount, rec.company_id.currency_id, rec.company_id, fields.Date.today())
                if rec.fees_account_id and (
                        rec.type == "out_invoice" or rec.type == "out_refund") and amount > 0:
                    if rec.type == "out_invoice":
                        already_exists.update({
                            'debit': amount < 0.0 and -amount or 0.0,
                            'credit': amount > 0.0 and amount or 0.0,
                        })
                    else:
                        already_exists.update({
                            'credit': amount < 0.0 and -amount or 0.0,
                            'debit': amount > 0.0 and amount or 0.0,
                        })
                total_balance = sum(other_lines.mapped('balance'))
                total_amount_currency = sum(other_lines.mapped('amount_currency'))
                terms_lines.update({
                    'amount_currency': -total_amount_currency,
                    'debit': total_balance < 0.0 and -total_balance or 0.0,
                    'credit': total_balance > 0.0 and total_balance or 0.0,
                })
            if not already_exists and rec.global_daraz_rate > 0:
                in_draft_mode = self != self._origin
                if not in_draft_mode and rec.type == 'out_invoice':
                    rec._recompute_universal_discount_lines()

    @api.onchange('global_daraz_rate', 'line_ids')
    def _recompute_universal_discount_lines(self):
        """This Function Create The General Entries for Daraz Fees"""
        for rec in self:

            type_list = ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']
            if rec.global_daraz_rate > 0 and rec.type in type_list:
                amount = 0
                if rec.is_invoice(include_receipts=True):
                    in_draft_mode = self != self._origin
                    name = "Daraz Fees"
                    value = "of amount #" + str(self.global_daraz_rate)
                    name = name + value
                    terms_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                    already_exists = self.line_ids.filtered(
                        lambda line: line.name and line.name.find('Daraz Fees') == 0)
                    if already_exists:
                        amount = self.daraz_fee
                        if self.fees_account_id \
                                and (self.type == "out_invoice"
                                     or self.type == "out_refund"):
                            if self.type == "out_invoice":
                                already_exists.update({
                                    'name': name,
                                    'debit': amount > 0.0 and amount or 0.0,
                                    'credit': amount < 0.0 and -amount or 0.0,
                                })
                            else:
                                already_exists.update({
                                    'name': name,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                    else:
                        new_tax_line = self.env['account.move.line']
                        create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create

                        if self.fees_account_id  and (self.type == "out_invoice" or self.type == "out_refund"):
                            amount = self.daraz_fee

                            dict = {
                                'move_name': self.name,
                                'name': name,
                                'price_unit': self.daraz_fee,
                                'quantity': 1,
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                                'account_id': self.fees_account_id,
                                'move_id': self._origin,
                                'date': self.date,
                                'exclude_from_invoice_tab': True,
                                'partner_id': terms_lines.partner_id.id,
                                'company_id': terms_lines.company_id.id,
                                'company_currency_id': terms_lines.company_currency_id.id,
                            }
                            if self.type == "out_invoice":
                                dict.update({
                                    'credit': amount > 0.0 and amount or 0.0,
                                    'debit': amount < 0.0 and -amount or 0.0,
                                })
                            else:
                                dict.update({
                                    'debit': amount < 0.0 and -amount or 0.0,
                                    'credit': amount > 0.0 and amount or 0.0,
                                })
                            if in_draft_mode:
                                
                                duplicate_id = self.invoice_line_ids.filtered(
                                    lambda line: line.name and line.name.find('Daraz Fees') == 0)
                                self.invoice_line_ids = self.invoice_line_ids - duplicate_id
                            else:
                                _logger.info("3.6")
                                dict.update({
                                    'price_unit': 0.0,
                                    'debit': 0.0,
                                    'credit': 0.0,
                                })
                                self.line_ids = [(0, 0, dict)]
                    if in_draft_mode:
                        # Update the payement account amount
                        terms_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                        other_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                        total_balance = sum(other_lines.mapped('balance'))
                        total_amount_currency = sum(other_lines.mapped('amount_currency'))
                        terms_lines.update({
                            'amount_currency': -total_amount_currency,
                            'debit': total_balance < 0.0 and -total_balance or 0.0,
                            'credit': total_balance > 0.0 and total_balance or 0.0,
                        })
                    else:
                        amount = rec.daraz_fee
                        currency_id = rec.currency_id
                        amount = currency_id._convert(amount, rec.company_id.currency_id, rec.company_id,
                                                      fields.Date.today())

                        terms_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                        other_lines = self.line_ids.filtered(
                            lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                        already_exists = self.line_ids.filtered(
                            lambda line: line.name and line.name.find('Daraz Fees') == 0)
                        total_balance = sum(other_lines.mapped('balance')) - amount
                        total_amount_currency = sum(other_lines.mapped('amount_currency'))
                        dict1 = {'credit': amount > 0.0 and amount or 0.0, 'debit': amount < 0.0 and -amount or 0.0}
                        dict2 = {'debit': total_balance < 0.0 and -total_balance or 0.0,
                                 'credit': total_balance > 0.0 and total_balance or 0.0}
                        if len(terms_lines) > 1:
                            amount = amount / len(terms_lines)
                            total_balance = sum(other_lines.mapped('balance')) + amount
                            dict2 = {'debit': total_balance < 0.0 and -total_balance or 0.0,
                                     'credit': total_balance > 0.0 and total_balance or 0.0}
                            # credits = terms_lines.mapped('credit')
                            # debits = terms_lines.mapped('debit')

                        self.with_context(check_move_validity=False).line_ids = [(1, already_exists.ids, dict1),
                                                                                 (1, terms_lines.ids, dict2)]  #
                        if len(rec.invoice_payment_term_id.line_ids) > 1:
                            old_payment_term = rec.invoice_payment_term_id
                            rec.invoice_payment_term_id = self.env.ref('account.account_payment_term_immediate')
                            rec.with_context(check_move_validity=False)._recompute_dynamic_lines()
                            rec.invoice_payment_term_id = old_payment_term
                            rec.with_context(check_move_validity=False)._recompute_dynamic_lines()

            elif self.global_daraz_rate <= 0:
                already_exists = self.line_ids.filtered(
                    lambda line: line.name and line.name.find('Daraz Fees') == 0)
                if already_exists:
                    self.line_ids -= already_exists
                    terms_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
                    other_lines = self.line_ids.filtered(
                        lambda line: line.account_id.user_type_id.type not in ('receivable', 'payable'))
                    total_balance = sum(other_lines.mapped('balance'))
                    total_amount_currency = sum(other_lines.mapped('amount_currency'))
                    terms_lines.update({
                        'amount_currency': -total_amount_currency,
                        'debit': total_balance < 0.0 and -total_balance or 0.0,
                        'credit': total_balance > 0.0 and total_balance or 0.0,
                    })