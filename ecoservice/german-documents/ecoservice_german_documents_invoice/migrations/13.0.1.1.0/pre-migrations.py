# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    model = env['ir.actions.report']
    def_invoice = env.ref(
        'account.account_invoices',
        False,
    ) or model
    def_invoice_wp = env.ref(
        'account.account_invoices_without_payment',
        False,
    ) or model

    gd_invoice = env.ref(
        'ecoservice_german_documents_invoice.report_invoice_report',
        False,
    ) or model
    gd_invoice_wp = env.ref(
        'ecoservice_german_documents_invoice.report_invoice_without_payment',
        False,
    ) or model

    email = env.ref('account.email_template_edi_invoice', False)

    if email and email.report_template == gd_invoice:
        email.report_template = def_invoice

    (gd_invoice | gd_invoice_wp).unlink_action()
    (def_invoice | def_invoice_wp).create_action()
