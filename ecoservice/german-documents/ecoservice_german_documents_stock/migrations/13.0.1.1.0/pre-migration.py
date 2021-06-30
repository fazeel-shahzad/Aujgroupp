# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    model = env['ir.actions.report']
    def_delivery = env.ref('stock.action_report_delivery', False) or model
    def_picking = env.ref('stock.action_report_picking', False) or model

    gd_delivery = env.ref(
        'ecoservice_german_documents_stock.report_stock_delivery_note',
        False,
    ) or model
    gd_delivery_wl = env.ref(
        'ecoservice_german_documents_stock.report_stock_delivery_note_no_logo',
        False,
    ) or model
    gd_picking = env.ref(
        'ecoservice_german_documents_stock.report_stock_picking_operation',
        False,
    ) or model
    gd_picking_wl = env.ref(
        'ecoservice_german_documents_stock.report_stock_picking_operation_no_logo',
        False,
    ) or model

    (gd_delivery | gd_picking).unlink_action()
    (def_picking | def_delivery | gd_delivery_wl | gd_picking_wl).create_action()
