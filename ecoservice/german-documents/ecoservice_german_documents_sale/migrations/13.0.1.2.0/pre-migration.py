
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    model = env['ir.actions.report']
    def_report = env.ref(
        'sale.action_report_saleorder',
        False,
    ) or model
    def_report_proforma = env.ref(
        'sale.action_report_pro_forma_invoice',
        False,
    ) or model

    gd_report = env.ref(
        'ecoservice_german_documents_sale.sale_order_report',
        False,
    ) or model
    gd_report_proforma = env.ref(
        'ecoservice_german_documents_sale.sale_order_report',
        False,
    ) or model

    email_template = env.ref('sale.email_template_edi_sale', False) or model

    if email_template and email_template.report_template == gd_report:
        email_template.report_template = def_report

    (gd_report | gd_report_proforma).unlink_action()
    (def_report | def_report_proforma).create_action()
