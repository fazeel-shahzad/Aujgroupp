# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
# from odoo.tools.misc import datetime
from datetime import datetime


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    payment_count = fields.Integer(compute='compute_payments')
    advance_payment = fields.Integer("Advance Payment", compute='compute_payments')

    @api.depends("partner_id")
    def compute_payments(self):
        obj = self.env['account.payment'].search_count([('so_number', '=', self.name)])
        if obj:
            self.payment_count = obj
        else:
            self.payment_count = 0
        count = self.env['account.payment'].search([('so_number', '=', self.name)],limit=1)
        self.advance_payment = count.amount

    def action_register_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apply Advance Payments',
            'view_id': self.env.ref('sale_order_payment.view_advance_payment_wizard_form', False).id,
            'context': {'default_ref': self.name, 'default_order_amount': self.amount_total, 'default_user_id': self.user_id.id},
            'target': 'new',
            'res_model': 'advance.payment.wizard',
            'view_mode': 'form',
        }

    def action_show_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Advance Payments',
            'view_id': self.env.ref('account.view_account_payment_tree', False).id,
            'target': 'current',
            'domain': [('communication', '=', self.name)],
            'res_model': 'account.payment',
            'views': [[False, 'tree'], [False, 'form']],
        }

    def action_confirm(self):
        flag = 0
        for rec in self:
            payments = self.env['account.payment'].search([('partner_id', '=', rec.partner_id.id), ('communication', '=', rec.name)])
            partner = self.env['res.partner'].search([('id', '=', rec.partner_id.id)], limit=1)
            print(partner.total_due)
            received_payment = 0
            for payment in payments:
                received_payment = received_payment + payment.amount
            if received_payment >= (rec.amount_total/2) or (partner.total_due*-1) >= (rec.amount_total/2):
                res = super(SaleOrderInh, self).action_confirm()
                flag = 1

        if flag == 0:
            raise UserError('There is no enough Advance Payment available to Confirm this Sale Order.')


#
# class StockPickingInh(models.Model):
#     _inherit = 'stock.picking'
#
#     state = fields.Selection([
#         ('draft', 'Draft'),
#         ('waiting', 'Waiting Another Operation'),
#         ('confirmed', 'Waiting'),
#         ('manager_approval', 'Approval from Manager'),
#         ('ceo_approval', 'Approval from CEO'),
#         ('reserve_manager_approvals', 'Reserve Approval from Manager'),
#         ('reserve_ceo_approval', 'Reserve Approval from CEO'),
#         ('assigned', 'Ready'),
#         ('done', 'Done'),
#         ('cancel', 'Cancelled'),
#     ], string='Status', compute='_compute_state',
#         copy=False, index=True, readonly=True, store=True, tracking=True,
#         help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
#              " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
#              " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
#              " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
#              " * Done: The transfer has been processed.\n"
#              " * Cancelled: The transfer has been cancelled.")
#     no_enough_amount = fields.Boolean(default=False, compute='compute_payment')
#
#     def compute_payment(self):
#         for rec in self:
#             partner = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
#             if partner:
#                 if abs(partner.total_due) >= (rec.sale_id.amount_total / 2):
#                     rec.no_enough_amount = False
#                 else:
#                     rec.no_enough_amount = True
#             else:
#                 rec.no_enough_amount = False
#
#
#     def action_reserve_do(self):
#         flag = 0
#         for rec in self:
#             partner = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
#             if partner:
#                 if abs(partner.total_due) >= (rec.sale_id.amount_total/2):
#                     rec.action_assign()
#                     flag = 1
#
#             if flag == 0:
#                 raise UserError('There is no enough Advance Payment available to Reserve this DO.')
#
#     def action_manager_approval(self):
#         self.state = 'ceo_approval'
#
#     def action_ceo_approval(self):
#         self.action_assign()
#
#     def action_get_approvals(self):
#         self.state = 'manager_approval'


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    advance_payment = fields.Float('Advance Payment', compute='compute_advance_payment')

    def compute_advance_payment(self):
        for rec in self:
            sale = self.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.advance_payment = sale.advance_payment


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    user_id = fields.Many2one('res.users')
    wiz_description = fields.Text('Description')
    cheque_no = fields.Char(string ="Cheque no")
    paid_by = fields.Char(string= "Paid by")
    received_by = fields.Char(string= "Received by")
    approved_by = fields.Char(string= "Paid by")
    so_number = fields.Char(string="SO Number")

    # def _compute_saleorder_number(self):
    #     for i in self:
    #         payments = self.env['sale.order'].search(
    #             [('name', '=', i.memo)])
    #         i.so_number=payments.name

    def get_amount_in_words(self,amount):
        amount_in_words = self.currency_id.amount_to_text(amount)
        amount_in_words = amount_in_words +" "+ "Only"
        return amount_in_words

