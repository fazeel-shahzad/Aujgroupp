# -*- coding: utf-8 -*-

from odoo import models, fields, api
from lxml import etree


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    driver_id = fields.Many2one('res.partner', 'Driver Name')
    mobile = fields.Char('Mobile', related='driver_id.mobile')
    vehicle_no = fields.Char('Vehicle No')
    note_del = fields.Char('Note')
    x_css = fields.Html(string='CSS', sanitize=False, compute='_compute_css', store=False)

    def _compute_css(self):
        for application in self:
            if self.env.user.has_group('warehouse_userright.group_remove_create_button') and application.state == 'confirmed':
                application.x_css = '<style>.o_form_button_edit {display: none !important;}</style>'
            else:
                application.x_css = False

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(StockPickingInh, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if self.env.user.has_group('warehouse_userright.group_remove_create_button'):
            temp = etree.fromstring(result['arch'])
            temp.set('create', '0')
            temp.set('delete', '0')
            result['arch'] = etree.tostring(temp)
        return result

    @api.onchange('move_line_ids_without_package')
    def onchange_move_line_ids_without_package(self):
        for rec in self:
            if len(rec.move_line_ids_without_package) > 1:
                for line in rec.move_line_ids_without_package:
                    if line.qty_done == 0:
                        line.qty_done = line.product_uom_qty
