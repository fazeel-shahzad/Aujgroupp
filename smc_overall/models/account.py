# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    customer_balance = fields.Float('Balance', compute='compute_customer_balance')

    def compute_customer_balance(self):
        for rec in self:
            invoices = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
            rec.customer_balance = invoices.total_due
