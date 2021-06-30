# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _recompute_global_discount_lines(self):
        ''' Compute the dynamic global discount lines of the journal entry.'''
        self.ensure_one()
        self = self.with_company(self.company_id)
        in_draft_mode = self != self._origin
        today = fields.Date.context_today(self)

        def _compute_payment_terms(self):
            sign = 1 if self.is_inbound() else -1

            IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
            discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
            if not discTax:
                discTax = 'untax'

            discount_balance = 0.0
            total_downpayment = 0.0
            total_downpayment_currency = 0.0
            currencies = set()
            for line in self.line_ids.filtered(
                    lambda l: l.sale_line_ids and l.sale_line_ids[0].is_downpayment):
                if line.currency_id:
                    currencies.add(line.currency_id)
                total_downpayment += line.balance
                total_downpayment_currency += line.amount_currency
            amount_downpayment = sign * (total_downpayment_currency if len(currencies) == 1 else total_downpayment)

            total = self.amount_untaxed + amount_downpayment + self.amount_tax
            if discTax != 'taxed':
                total = self.amount_untaxed + amount_downpayment

            if self.global_discount_type == 'fixed':
                discount_balance = sign * (self.global_order_discount or 0.0)
            else:
                discount_balance = sign * (total * (self.global_order_discount or 0.0) / 100)

            if self.currency_id == self.company_id.currency_id:
                discount_amount_currency = discount_balance
            else:
                discount_amount_currency = discount_balance
                discount_balance = self.currency_id._convert(
                    discount_amount_currency, self.company_id.currency_id, self.company_id, self.date)

            if self.invoice_payment_term_id:
                date_maturity = self.invoice_date or today
            else:
                date_maturity = self.invoice_date_due or self.invoice_date or today
            return [(date_maturity, discount_balance, discount_amount_currency)]

        def _compute_diff_global_discount_lines(self, existing_global_lines, account, to_compute):
            new_global_discount_lines = self.env['account.move.line']
            for date_maturity, balance, amount_currency in to_compute:
                if existing_global_lines:
                    candidate = existing_global_lines[0]
                    candidate.update({
                        'date_maturity': date_maturity,
                        'amount_currency': amount_currency,
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                    })
                else:
                    create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                    candidate = create_method({
                        'name': 'Global Discount',
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                        'quantity': 1.0,
                        'amount_currency': amount_currency,
                        'date_maturity': date_maturity,
                        'move_id': self.id,
                        'currency_id': self.currency_id.id if self.currency_id != self.company_id.currency_id else False,
                        'account_id': account.id,
                        'partner_id': self.commercial_partner_id.id,
                        'exclude_from_invoice_tab': True,
                        'is_global_line': True,
                    })
                new_global_discount_lines += candidate
                if in_draft_mode:
                    candidate.update(candidate._get_fields_onchange_balance())
            return new_global_discount_lines

        existing_global_lines = self.line_ids.filtered(lambda line: line.is_global_line)
        others_lines = self.line_ids.filtered(lambda line: not line.is_global_line)

        if not others_lines:
            self.line_ids -= existing_global_lines
            return

        if existing_global_lines:
            account = existing_global_lines[0].account_id
        else:
            IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
            if self.move_type in ['out_invoice', 'out_refund', 'out_receipt']:
                account = self.env.company.discount_account_invoice
            else:
                account = self.env.company.discount_account_bill
            if not account:
                raise UserError(
                    _("Global Discount!\nPlease first set account for global discount in account setting."))

        to_compute = _compute_payment_terms(self)

        new_terms_lines = _compute_diff_global_discount_lines(self, existing_global_lines, account, to_compute)

        self.line_ids -= existing_global_lines - new_terms_lines
