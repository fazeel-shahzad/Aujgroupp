# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class JoltaManufacturingInh(models.Model):
    _inherit = 'material.purchase.requisition'

    ref = fields.Char('Reference')
    is_internal_transfer_done = fields.Boolean(compute='compute_transfer_done')
    is_created_by_store = fields.Boolean()

    def compute_transfer_done(self):
        transfers = self.env['stock.picking'].search([('custom_requisition_id', '=', self.id)])
        flag = True
        for rec in transfers:
            if rec.state != 'done':
                flag = False
        if flag:
            self.is_internal_transfer_done = True
        else:
            self.is_internal_transfer_done = False

    @api.onchange('dest_location_id')
    def onchange_get_invoices(self):
        locations = self.env['stock.location'].search([('user_id', '=', self.env.user.id)])
        return {'domain': {'dest_location_id': [('id', 'in', locations.ids)]}}


class JoltaManufacturingLineInh(models.Model):
    _inherit = 'material.purchase.requisition.line'

    requisition_type = fields.Selection(
        selection=[('internal', 'Internal Picking'),
                   ('purchase', 'Purchase Order'),
        ], string='Requisition Action', default='internal', required=True,)
    issued_qty = fields.Float('Issued Qty')
    short_qty = fields.Float('Shortage', compute='compute_short_qty')

    def compute_short_qty(self):
        for rec in self:
            rec.short_qty = rec.qty - rec.issued_qty


class StockMoveLineInh(models.Model):
    _inherit = 'stock.move.line'

    is_immediate = fields.Boolean(compute='_compute_is_immediate')
    reason_of_rejection = fields.Char('Reason of Rejection')
    observation = fields.Char('Observation')
    qty_store = fields.Integer('Qty submitted to Store ')
    return_vendor = fields.Integer('Return to Vendor')
    material_received = fields.Integer('Material Received Against Rejection Line')

    def _compute_is_immediate(self):
        for rec in self:
            print(rec.picking_id.immediate_transfer)
            if rec.picking_id.immediate_transfer:
                rec.is_immediate = False
            else:
                rec.is_immediate = True

    # @api.onchange('reason_of_rejection')
    # def onchange_source(self):
    #     print("Hello")
    #     print(self.picking_id.immediate_transfer)


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    # is_internal_transfer = fields.Boolean(compute='_compute_immediate_transfer')
    #
    # def _compute_immediate_transfer(self):
    #     for rec in self:
    #         print(rec.immediate_transfer)
    #         if rec.immediate_transfer:
    #             rec.is_internal_transfer = True
    #         else:
    #             rec.is_internal_transfer = False

    req_count = fields.Integer(compute="compute_req_count", string="Requisitions")

    def compute_req_count(self):
        for rec in self:
            count = self.env['material.purchase.requisition'].search_count([('ref', '=', rec.name)])
            rec.req_count = count

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('purchase_waiting', 'p Waiting'),
        ('assigned', 'Ready'),
        ('sent_approve', 'Sent for Approval'),
        ('qc', 'Quality'),
        ('qc_approved', 'Quality Approved'),
        ('approval', 'Waiting For Approval'),
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

    section_id = fields.Many2one('stock.location')
    model = fields.Char('Model')
    color = fields.Char('Color')
    lot_no = fields.Char('Lot No')
    lot_qty = fields.Char('Lot Qty')
    work_order = fields.Char('Work Order #')
    work_order_qty = fields.Char('Work Order Qty')
    date_approval = fields.Date()
    backorder_count = fields.Integer(compute='_compute_backorders')
    is_greater_done = fields.Boolean(compute="compute_qty")
    is_grn_approved = fields.Boolean()
    is_req_created = fields.Boolean()

    is_store_user = fields.Boolean(default=False, compute='compute_store_user')
    is_purchase_user = fields.Boolean(compute='compute_store_user')

    def compute_store_user(self):
        if self.env.user.has_group('jolta_manufacturing.group_internal_transfer_store_user'):
            self.is_store_user = True
        else:
            self.is_store_user = False
        if self.env.user.has_group('jolta_manufacturing.group_immediate_transfer_purchase_user'):
            self.is_purchase_user = True
        else:
            self.is_purchase_user = False

    def create_requisition(self):
        dest_loc = self.env['stock.location'].search([('user_id','=', self.env.user.id)])
        line_vals = []
        for line in self.move_ids_without_package:
            if line.reserved_availability < line.product_uom_qty:
                line_vals.append((0, 0, {
                    'requisition_type': 'internal',
                    'product_id': line.product_id.id,
                    'description': line.product_id.name,
                    'qty':  line.product_uom_qty - line.reserved_availability,
                    'uom': line.product_id.uom_id.id,
                }))
                line_vals.append(line_vals)
        vals = {
            'company_id': self.env.user.company_id.id,
            'request_date': fields.Date.today(),
            'dest_location_id': dest_loc.id,
            'requisition_line_ids': line_vals,
            'ref': self.name,
            'is_created_by_store': True,
            }
        move = self.env['material.purchase.requisition'].create(vals)
        self.is_req_created = True
        if self.is_store_user:
            self.state = 'purchase_waiting'

    def action_show_requisitions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Requisitions',
            'view_id': self.env.ref('material_purchase_requisitions.material_purchase_requisition_tree_view', False).id,
            'target': 'current',
            'domain': [('ref', '=', self.name)],
            'res_model': 'material.purchase.requisition',
            'views': [[False, 'tree'], [False, 'form']],
        }

    @api.depends('move_ids_without_package.quantity_done')
    def compute_qty(self):
        for line in self.move_ids_without_package:
            if line.product_uom_qty + ((line.product_uom_qty / 100)*5) < line.quantity_done:
                self.is_greater_done = True
            else:
                self.is_greater_done = False

    def _compute_backorders(self):
        count = self.env['stock.picking'].search_count([('backorder_id', '=', self.id)])
        self.backorder_count = count

    def reject_grn(self):
        for rec in self:
            rec.state = 'assigned'

    def approve_grn(self):
        for rec in self:
            rec.is_grn_approved = True
            rec.state = 'assigned'

    def send_approval(self):
        for rec in self:
            rec.state = 'sent_approve'

    def reject(self):
        for rec in self:
            rec.state = 'draft'

    def approve(self):
        res = super(StockPickingInh, self).button_validate()
        req = self.env['stock.picking'].search([('name', '=', self.custom_requisition_id.ref)])
        if req:
            req.state = 'waiting'
        return res

    def approve_quality(self):
        self.state = 'qc_approved'
        self.state = 'approval'

    def button_validate(self):
        for rec in self:
            if rec.env.user.company_id.id == 24:
                if rec.picking_type_id.code == 'internal':
                    if rec.immediate_transfer:
                        rec.state = 'qc'
                    else:
                        rec.state = 'approval'
                        rec.date_approval = datetime.date.today()
                else:
                    for line in rec.move_ids_without_package:
                        if line.product_uom_qty + ((line.product_uom_qty / 100)*5) < line.quantity_done and rec.is_grn_approved == False:
                            # rec.is_greater_done = True
                            raise UserError(("Done Quantity Connot be greater than 5% of Demand Quantity"))
                    return super(StockPickingInh, self).button_validate()
            else:
                rec = super(StockPickingInh, self).button_validate()

    def get_source_document(self):
        doc = []
        if self.backorder_id:
            back_order = self.env['stock.picking'].search([('id', '=', self.backorder_id.id)])
            if back_order:
                for rec in back_order:
                    doc.append(rec.name)
            doc.append(self.name)
        else:
            doc.append(self.name)
            back_order = self.env['stock.picking'].search([('backorder_id', '=', self.id)])
            if back_order:
                for rec in back_order:
                    doc.append(rec.name)
        my_string = ', '.join(doc)
        return my_string

    def get_approval_date(self, line):
        if line.picking_id.state == 'done':
            return line.picking_id.date_approval
        else:
            return ''

    def get_backorder_approval_date(self, line):
        back_order = self.env['stock.picking'].search([('backorder_id', '=', self.id)])
        date = ''
        if back_order:
            for rec in back_order.move_ids_without_package:
                if rec.product_id.id == line.product_id.id and back_order.state == 'done':
                    date = back_order.date_approval
        return date

    def get_backorder_line(self, line):
        back_order = self.env['stock.picking'].search([('backorder_id', '=', self.id)])
        name = ''
        if back_order:
            for rec in back_order.move_ids_without_package:
                if rec.product_id.id == line.product_id.id and back_order.state == 'done':
                    name = back_order.location_dest_id.user_id.name
        return name

    def get_shortage(self, line):
        back_order = self.env['stock.picking'].search([('backorder_id', '=', self.id)])
        qty = 0
        if back_order:
            for rec in back_order.move_ids_without_package:
                if line.product_id.id == rec.product_id.id:
                    qty = qty + rec.product_uom_qty
        return qty

    def action_backorder_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Backorders',
            'view_id': self.env.ref('stock.vpicktree', False).id,
            'target': 'current',
            'domain': [('backorder_id', '=', self.id)],
            'res_model': 'stock.picking',
            'views': [[False, 'tree'], [False, 'form']],
        }


class InternalTransferApproval(models.Model):
    _inherit = 'stock.location'

    user_id = fields.Many2many('res.users', string='User Id')


class MrpManufacturingInh(models.Model):
    _inherit = 'mrp.production'

    is_req_created = fields.Boolean()
    req_count = fields.Integer(compute="compute_req_count", string="Requisitions")

    def _get_default_location_src_id(self):
        loc = self.env['stock.location'].search([('user_id', '=', self.env.user.id)])
        return loc

    def _get_default_location_dest_id(self):
        loc = self.env['stock.location'].search([('user_id', '=', self.env.user.id)])
        return loc

    location_src_id = fields.Many2one(
        'stock.location', 'Components Location',
        default=_get_default_location_src_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will look for components.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Finished Products Location',
        default=_get_default_location_dest_id,
        readonly=True, required=True,
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        states={'draft': [('readonly', False)]}, check_company=True,
        help="Location where the system will stock the finished products.")

    # @api.onchange('location_src_id')
    # def onchange_get_invoices(self):
    #     locations = self.env['stock.location'].search([('user_id', '=', self.env.user.id)])
    #     return {'domain': {'dest_location_id': [('id', 'in', locations.ids)]}}

    def compute_req_count(self):
        for rec in self:
            count = self.env['material.purchase.requisition'].search_count([('ref', '=', rec.name)])
            print(count)
            rec.req_count = count

    def action_show_requisitions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Requisitions',
            'view_id': self.env.ref('material_purchase_requisitions.material_purchase_requisition_tree_view', False).id,
            'target': 'current',
            'domain': [('ref', '=', self.name)],
            'res_model': 'material.purchase.requisition',
            'views': [[False, 'tree'], [False, 'form']],
        }

    def action_create_requisition(self):
        product_list = []
        bom = self.env['mrp.bom'].search([])
        for rec in bom:
            product_list.append(rec.product_tmpl_id.id)
        line_vals = []
        for line in self.move_raw_ids:
            if line.product_id.product_tmpl_id.id not in product_list and line.reserved_availability < line.product_uom_qty:
                line_vals.append((0, 0, {
                    'requisition_type': 'internal',
                    'product_id': line.product_id.id,
                    'description': line.product_id.name,
                    'qty':  line.product_uom_qty - line.reserved_availability,
                    'uom': line.product_id.uom_id.id,
                }))
                line_vals.append(line_vals)
        vals = {
            'company_id': self.env.user.company_id.id,
            'request_date': fields.Date.today(),
            'requisition_line_ids': line_vals,
            'ref': self.name,
            }
        move = self.env['material.purchase.requisition'].create(vals)
        self.is_req_created = True



