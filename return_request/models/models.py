# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.float_utils import float_round
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class ReturnRequest(models.Model):
    _name = 'returns.bash'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Return Request'
    _rec_name = 'partner_id'
    _order = 'id desc'

    partner_id = fields.Many2one("res.partner", string="Customer Name")
    contact_person_id = fields.Many2one("res.partner", string="Contact Person",
                                        domain="[('id', 'child_of',partner_id)]")
    address = fields.Char(string="Address")
    date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now())
    net_total = fields.Integer("Net Total", compute="compute_total_invoice")
    request_lines = fields.One2many("request.line", "request_order_id")
    state = fields.Selection([('user', 'User'), ('manager', 'Manager'), ('director', 'Director'), ('approved', 'Approved'), ('done', 'Validated'),
                              ('rejected', 'Rejected')], string="State", readonly=True, default="user", tracking=1)
    is_check_qty = fields.Boolean(default=False, compute='compute_check_quantity')
    is_sent_for_second_approval = fields.Boolean(default=False)
    is_second_approved = fields.Boolean(default=False)

    def compute_check_quantity(self):
        if self.request_lines:
            for rec in self.request_lines:
                if rec.return_quantity == rec.recieved_qty:
                    self.is_check_qty = False
                elif self.is_second_approved == True:
                    self.is_check_qty = False
                else:
                    self.is_check_qty = True
        else:
            self.is_check_qty = True

    def action_second_approval_from_manager(self):
        self.state = 'manager'
        self.is_sent_for_second_approval = True

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'

    def action_manager_approval(self):
        if self.is_sent_for_second_approval:
            self.is_second_approved = True
            self.state = 'director'
        else:
            self.state = 'director'

    def action_draft(self):
        self.state = 'user'

    def action_validate(self):
        if self.is_check_qty == False:
            invoices_list = []
            for rec in self.request_lines:
                invoices_list.append(rec.invoice_id.id)
            products_list = []
            invoices_list = list(dict.fromkeys(invoices_list))
            for inv in invoices_list:
                for line in self.request_lines:
                    if line.invoice_id.id == inv:
                        products_list.append(line.product_id.id)
            # products_list = list(dict.fromkeys(products_list))
            self.create_delivery(invoices_list)
            self.create_invoice(invoices_list)
            # self.create_scrap(products_list)
            self.state = 'done'
        else:
            raise UserError("Please Get Approval From Manager.")

    # def create_scrap(self, products_list):
    #     products = self.env['product.product'].browse(products_list)
    #     picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
    #     for rec in products:
    #         lines = self.env['request.line'].search([('product_id', '=', rec.id), ('request_order_id', '=', self.id)])
    #         qty = 0
    #         vals = {}
    #         for line in lines:
    #             # if line.product_id.name == rec.name:
    #             qty = qty + line.recieved_qty
    #             sale_order = line.invoice_id.invoice_origin
    #             delivery = self.env['stock.picking'].search([('partner_id', '=', self.partner_id.id), ('picking_type_id', '=', picking_incoming.id)])
    #             vals = {
    #                 'product_id': line.product_id.id,
    #                 'origin': sale_order,
    #                 'picking_id': delivery[0].id,
    #                 'date_done': datetime.today().date(),
    #                 'scrap_qty': qty,
    #                 'product_uom_id': line.product_id.uom_id.id,
    #             }
    #         scrap = self.env['stock.scrap'].create(vals)
    #         scrap.do_scrap()

    def create_invoice(self, invoices_list):
        record = self.env['account.account'].search([])[0]
        invoices = self.env['account.move'].browse(invoices_list)
        for rec in invoices:
            ref = ''
            lines = self.env['request.line'].search([('invoice_id', '=', rec.id), ('request_order_id', '=', self.id)])
            line_vals = []
            for line in lines:
                if line.invoice_id.name == rec.name:
                    line_vals.append((0, 0, {
                        'product_id': line.product_id.id,
                        'price_unit': line.unit_price,
                        'quantity': line.return_quantity,
                        'account_id': record.id
                    }))
                    ref = line.invoice_id.name
                    sale_order = line.invoice_id.invoice_origin
                line_vals.append(line_vals)
            inv = self.env['account.move'].search([('name', '=', ref)])
            order = self.env['sale.order'].search([('name', '=', sale_order)])
            vals = {
                'partner_id': self.partner_id.id,
                'invoice_date': datetime.today().date(),
                'move_type': 'out_refund',
                'invoice_line_ids': line_vals,
                'state': 'draft',
                'invoice_origin': order.name,
                'partner_shipping_id': order.partner_invoice_id.id,
                'reversed_entry_id': inv.id,
                'ref': _("Reversal of %s", ref)
            }
            move = self.env['account.move'].create(vals)
            move.action_post()
            print("Invoice Generated!!!!!!")

    def create_delivery(self, invoices_list):
        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        invoices = self.env['account.move'].browse(invoices_list)
        for rec in invoices:
            request_lines = self.env['request.line'].search(
                [('invoice_id', '=', rec.id), ('request_order_id', '=', self.id)])
            line_vals = []
            for line in request_lines:
                sale_order = line.invoice_id.invoice_origin
                delivery = self.env['stock.picking'].search([('origin', '=', sale_order)])
                if len(delivery) > 1:
                    delivery = delivery[0]
                sale_order = self.env['procurement.group'].search([('name', '=', sale_order)])
                if line.invoice_id.name == rec.name:
                    line_vals.append((0, 0, {
                        'product_id': line.product_id.id,
                        'name': 'Transfer In',
                        'product_uom': line.product_id.uom_id.id,
                        'location_id': delivery.location_dest_id.id,
                        'location_dest_id': delivery.location_id.id,
                        'product_uom_qty': line.return_quantity,
                        'quantity_done': line.return_quantity,
                        'group_id': sale_order.id
                    }))
            new_picking = delivery.copy({
                'move_lines': [],
                'picking_type_id': picking_incoming.id,
                'state': 'done',
                'origin': _("Return of %s", delivery.name),
                'location_id': delivery.location_dest_id.id,
                'location_dest_id': delivery.location_id.id,
                'group_id': sale_order.id
            })
            new_picking.write({
                'move_lines': line_vals,
            })
            new_picking.action_confirm()
            new_picking.button_validate()
            return new_picking

    def action_confirmed(self):
        for i in self:
            i.state = 'manager'

    def action_done(self):
        for i in self:
            i.state = 'director'

    @api.onchange("name")
    def onchange_partner_id(self):
        self.address = self.name.street

    @api.depends("request_lines.total")
    def compute_total_invoice(self):
        total = 0
        for i in self.request_lines:
            total = total + i.total
        self.update({
            'net_total': total})


class ReturnRequested(models.Model):
    _name = 'request.line'
    _description = 'Return Request Line'

    request_order_id = fields.Many2one("returns.bash")
    invoice_date = fields.Date("Invoice Date", readonly=True, related='invoice_id.invoice_date')
    invoice_id = fields.Many2one("account.move")
    product_id = fields.Many2one("product.product", string="Item Description")
    art = fields.Char("Art", related='product_id.article_no')
    sold_quantity = fields.Integer("Sold Qty", compute='compute_sold_quantity')
    previous_return_quantity = fields.Integer("Previous Return Qty")
    return_quantity = fields.Integer("Return Qty")
    discount_qty = fields.Float("Discount")
    unit_price = fields.Integer("Unit Price")
    total = fields.Float("Total", compute='compute_total')
    reason_of_return = fields.Char("Reason Of Return")
    finish_no = fields.Char('Finish No', related='product_id.finish_no')
    recieved_qty = fields.Integer('Received Qty')
    state = fields.Selection(
        [('user', 'User'), ('manager', 'Manager'), ('director', 'Director'), ('approved', 'Approved'),
         ('done', 'Validate'),
         ('rejected', 'Rejected')], string="State", readonly=True, default="user", related='request_order_id.state')


    @api.onchange('return_quantity')
    def verify_return_quantity(self):
        for rec in self:
            if rec.return_quantity:
                sale_order = rec.invoice_id.invoice_origin
                group_id = self.env['procurement.group'].search([('name', '=', sale_order)])
                picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
                deliveries = self.env['stock.picking'].search([('partner_id', '=', rec.request_order_id.partner_id.id),
                                                               ('picking_type_id', '=', picking_incoming.id),
                                                               ('group_id', '=', group_id.id)])
                delivered_quantity = 0
                if deliveries:
                    for delivery in deliveries:
                        for line in delivery.move_ids_without_package:
                            delivered_quantity = delivered_quantity + line.quantity_done
                    rec.previous_return_quantity = delivered_quantity
                    total_returned = rec.previous_return_quantity + rec.return_quantity
                    if total_returned > rec.sold_quantity:
                        raise UserError('Sold Quantity is Already Returned')

    @api.onchange('return_quantity')
    def compute_total(self):
        for rec in self:
            rec.total = (rec.return_quantity * rec.unit_price) - rec.discount_qty

    @api.onchange('product_id')
    def compute_sold_quantity(self):
        for rec in self:
            qty = ''
            price_unit = ''
            discount = ''
            for line in rec.invoice_id.invoice_line_ids:
                if line.product_id.id == rec.product_id.id:
                    qty = line.quantity
                    price_unit = line.price_unit
                    discount = line.discount
            rec.sold_quantity = qty
            rec.unit_price = price_unit
            rec.discount_qty = discount

    @api.onchange('invoice_id')
    def onchange_get_invoices(self):
        invoices = self.env['account.move'].search(
            [('partner_id', '=', self.request_order_id.partner_id.id), ('move_type', '=', 'out_invoice')])
        self.product_id = ''
        return {'domain': {'invoice_id': [('id', 'in', invoices.ids)]}}

    @api.onchange('invoice_id')
    def onchange_get_products(self):
        product_list = []
        for rec in self.invoice_id.invoice_line_ids:
            if rec.product_id.type == 'product':
                product_list.append(rec.product_id.id)
        return {'domain': {'product_id': [('id', 'in', product_list)]}}
