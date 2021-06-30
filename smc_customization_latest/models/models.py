# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError



class smc(models.Model):
    _inherit = 'product.template'

    sale_discontinued=fields.Boolean("Sales Discontinued Products", compute="_on_hand")


    def _on_hand(self):
        for i in self:
            if i.qty_available <= 0:
                i.sale_discontinued=True
                i.sale_ok = False
            else:
                i.sale_discontinued = False


# class smc(models.Model):
#     _inherit = 'stock.picking'

#     invoice_status = fields.Selection([('paid', 'Paid'), ('not_paid', 'Not Paid')], string="Invoice Status", compute="_check_status")

#     def _check_status(self):
#         for i in self:
#             search_invoice = self.env['account.move'].search([('invoice_origin', '=', i.origin)], limit=1)
#             if search_invoice.payment_state in ['paid','','in_payment']:
#                 i.invoice_status="paid"
#             else:
#                 i.invoice_status = "not_paid"


class in_invoicing(models.Model):
    _inherit = 'account.move'

    delivery_order = fields.Char(string='DO Number',compute='_compute_global')

    check_status = fields.Selection([('credit_approval', 'Ask for Credit Approval'), ('approved', 'Credit Approved')], string="Check Status", readonly=True,compute="Check_status_payment")

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),('credit_approval', 'Ask for Credit Approval'), ('approved', 'Credit Approved')
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    def action_approve(self):
            self.state = 'approved'

    def Check_status_payment(self):
        for i in self:
            print(i.state)
            if  i.state in ['approved'] or i.payment_state in ['paid','partial','in_payment']:
                i.check_status='approved'
            else:
                i.check_status ='credit_approval'



    def action_ask_for_approval(self):
        self.state ='credit_approval'

    def _compute_global(self):
        for i in self:
            record = self.env['stock.picking'].search([('origin', '=', i.invoice_origin)],limit=1)
            i.delivery_order = record.name




class SaleOrder(models.Model):
    _inherit = 'sale.order'


    payment_status = fields.Selection([('paid', 'Paid'), ('not_paid', 'Not Paid')], string="Payment Status", compute="_check_status")



    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('manager', 'Approval from Manager'),('ceo', 'Approval from CEO'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    max_discount = fields.Float(string='Max Disccount', compute='compute_max_disccount', default=0)

    allowed_discount = fields.Float(string='Allowed Disccount', related='user_id.allowed_discount')
    user_id = fields.Many2one('res.users', string='User',compute="compute_self_id")


    def compute_self_id(self):
        self.user_id=self.env.uid

    def from_manager_approval(self):
        self.state='manager'

    def from_ceo_approval(self):
        self.state='ceo'

    def _check_status(self):
        for i in self:
            search_invoice = self.env['account.move'].search([('invoice_origin', '=', i.name)], limit=1)
            print("search_invoice.state ",search_invoice.state)
            print(search_invoice.invoice_origin)
            if search_invoice.payment_state in ['paid','partial','in_payment'] or search_invoice.state in ['approved']:
                i.payment_status="paid"
            else:
                i.payment_status = "not_paid"



    def action_confirm(self):
        for sale_order in self:
            print("Helloo")

            if sale_order.max_discount > sale_order.allowed_discount:

                raise UserError(_('Your discount limit is lesser then allowed discount.Click on "Ask for Approval" for approval'))

        return super(SaleOrder, self).action_confirm()


    @api.onchange("order_line.discount")
    def compute_max_disccount(self):

        record = self.env['sale.order'].search([])
        for i in record:
            maximum = []
            diss=0.0
            for rec in i.order_line:
                maximum.append(rec.discount)
            print(maximum)
            if maximum:
                diss = max(maximum)
                i.max_discount = diss
            else:
                i.max_discount = 0


class users_inherit(models.Model):
    _inherit = 'res.users'
    _description = 'adding to users table'

    allowed_discount = fields.Float(string='Discount Allowed')


