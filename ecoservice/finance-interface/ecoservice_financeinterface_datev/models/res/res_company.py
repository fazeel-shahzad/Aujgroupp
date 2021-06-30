# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # region Fields
    datev_export_method = fields.Selection(
        selection=[
            ('gross', 'gross'),
            ('net', 'net'),
        ],
        string='Export method',
        default='gross',
    )
    datev_ignore_currency = fields.Boolean(
        string='Ignore Currency',
        help="If set the export currency will always be the company's default currency",
    )
    l10n_de_datev_consultant_number = fields.Char(
        string='Consultant No.',
        size=7,
    )
    l10n_de_datev_client_number = fields.Char(
        string='Client No.',
        size=5,
    )
    datev_group_lines = fields.Boolean(
        string='Group Move Lines',
        default=True,
    )
    datev_group_sh = fields.Boolean(
        string='Combine Credit & Debit',
        default=True,
    )
    account_code_digits = fields.Integer(
        string='Number of digits in an account code',
    )
    # endregion
