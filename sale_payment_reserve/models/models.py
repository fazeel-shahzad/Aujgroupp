# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    payment_count = fields.Integer(compute='compute_payments')

    def compute_payments(self):
        for rec in self:
            count = self.env['account.payment'].search_count([('ref', '=', rec.name)])
            rec.payment_count = count

    def action_register_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Apply Advance Payments',
            'view_id': self.env.ref('sale_payment_reserve.view_advance_payment_wizard_form', False).id,
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
            'domain': [('ref', '=', self.name)],
            'res_model': 'account.payment',
            'views': [[False, 'tree'], [False, 'form']],
        }

    def action_confirm(self):
        res = super(SaleOrderInh, self).action_confirm()
        for order in self:
            for picking in order.picking_ids:
                picking.do_unreserve()
        return res


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('manager_approval', 'Approval from Manager'),
        ('ceo_approval', 'Approval from CEO'),
        ('reserve_manager_approvals', 'Reserve Approval from Manager'),
        ('reserve_ceo_approval', 'Reserve Approval from CEO'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")
    no_enough_amount = fields.Boolean(default=False, compute='compute_payment')

    def compute_payment(self):
        for rec in self:
            partner = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
            if partner:
                if abs(partner.total_due) >= (rec.sale_id.amount_total / 2):
                    rec.no_enough_amount = False
                else:
                    rec.no_enough_amount = True
            else:
                rec.no_enough_amount = False


    def action_reserve_do(self):
        flag = 0
        for rec in self:
            partner = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
            if partner:
                if abs(partner.total_due) >= (rec.sale_id.amount_total/2):
                    rec.action_assign()
                    flag = 1

            if flag == 0:
                raise UserError('There is no enough Advance Payment available to Reserve this DO.')

    def action_manager_approval(self):
        self.state = 'ceo_approval'

    def action_ceo_approval(self):
        self.action_assign()

    def action_get_approvals(self):
        self.state = 'manager_approval'


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    user_id = fields.Many2one('res.users', related="partner_id.user_id")
