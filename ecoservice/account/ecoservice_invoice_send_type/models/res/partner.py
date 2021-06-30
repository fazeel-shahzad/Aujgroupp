# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_send_type = fields.Selection(
        selection=[
            ('print', 'Print'),
            ('email', 'Email'),
        ],
        help='Determine the way of sending an invoice. '
             'Selecting a type restricts the way of sending an invoice to this customer. '
             'If this field is left empty all options are avaiblable in the invoice.')
