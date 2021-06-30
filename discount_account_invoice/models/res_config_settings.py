# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_order_global_discount = fields.Boolean(
        string="A global discount on invoices/bills",
        implied_group='discount_account_invoice.group_order_global_discount',
        config_parameter='account.group_order_global_discount',
        help="Allows to give a global discount on invoice/bills. ")
    global_discount_tax = fields.Selection(
        selection=[('untax', 'Untaxed amount'), ('taxed', 'Tax added amount')],
        string="Global Discount Calculation",
        default="untax",
        help="Global disount calculation will be ( \
             'untax' : Global discount will be applied before applying tax, \
             'taxed : Global disount will be applied after applying tax)")
    discount_account_invoice = fields.Many2one(
        string="Invoice Discount Account",
        comodel_name='account.account',
        related="company_id.discount_account_invoice",
        readonly=False,
        help="Account for Global discount on invoices.")
    discount_account_bill = fields.Many2one(
        string="Bill Discount Account",
        comodel_name='account.account',
        related="company_id.discount_account_bill",
        readonly=False,
        help="Account for Global discount on bills.")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        IrConfigPrmtr.set_param('account.group_order_global_discount',
                                self.group_order_global_discount)
        IrConfigPrmtr.set_param('account.global_discount_tax',
                                self.global_discount_tax)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        group_order_global_discount = IrConfigPrmtr.get_param(
            'account.group_order_global_discount')
        global_discount_tax = IrConfigPrmtr.get_param(
            'account.global_discount_tax')
        res.update({
            'group_order_global_discount': group_order_global_discount,
            'global_discount_tax': global_discount_tax,
        })
        return res
