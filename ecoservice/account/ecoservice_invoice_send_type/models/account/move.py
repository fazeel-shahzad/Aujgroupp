# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_send_type = fields.Selection(
        selection=[
            ('print', 'Print'),
            ('email', 'Email')
        ],
        help='Determine the way of sending an invoice. '
             'Selecting a type restricts the way of sending an invoice to this customer. '
             'If this field is left empty all options are avaiblable in the invoice.'
    )

    def default_invoice_send_type(self):
        for invoice in self:
            invoice.invoice_send_type = (
                invoice.partner_id.invoice_send_type
                or invoice.partner_id.parent_id.invoice_send_type
            )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        self.default_invoice_send_type()
        return res

    @api.model
    def create(self, vals):
        """Add a 'Invoice Send Type' to the invoice."""
        invoice = super(AccountMove, self).create(vals)
        invoice.invoice_send_type = (
            invoice.partner_id.invoice_send_type
            or invoice.partner_id.parent_id.invoice_send_type
        )
        return invoice
