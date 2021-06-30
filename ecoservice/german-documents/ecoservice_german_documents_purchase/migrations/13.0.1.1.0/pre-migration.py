# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    model = env['ir.actions.report']
    def_report_quotation = env.ref(
        'purchase.report_purchase_quotation',
        False,
    ) or model
    def_report_order = env.ref(
        'purchase.action_report_purchase_order',
        False,
    ) or model

    gd_report = env.ref(
        'ecoservice_german_documents_purchase.report_purchase_order_quotation',
        False,
    ) or model

    email_rfq = env.ref('purchase.email_template_edi_purchase', False) or model
    email_order = env.ref('purchase.email_template_edi_purchase_done', False) or model

    if email_rfq and email_rfq.report_template == gd_report:
        email_rfq.report_template = def_report_quotation

    if email_order and email_order.report_template == gd_report:
        email_order.report_template = def_report_order

    gd_report.unlink_action()
    (def_report_quotation | def_report_order).create_action()
