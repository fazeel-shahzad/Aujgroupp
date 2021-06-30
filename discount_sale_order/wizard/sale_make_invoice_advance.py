# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _get_advance_details(self, order):
        if order.global_order_discount:
            IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
            discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
            if discTax == 'taxed':
                total = order.amount_untaxed + order.amount_tax
            else:
                total = order.amount_untaxed
            if order.global_discount_type == 'fixed':
                total -= order.global_order_discount
            else:
                total *= (1 - (order.global_order_discount or 0.0) / 100)
            if discTax == 'taxed':
                total -= order.amount_tax
            if self.advance_payment_method == 'percentage':
                amount = total * self.amount / 100
                name = _("Down payment of %s%%") % (self.amount)
            else:
                amount = self.fixed_amount
                name = _('Down Payment')
            return amount, name
        else:
            return super(SaleAdvancePaymentInv, self)._get_advance_details(order)
