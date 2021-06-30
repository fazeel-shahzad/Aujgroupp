# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # region Fields
    account_code_digits = fields.Integer(
        related='company_id.account_code_digits',
        readonly=False,
    )

    datev_export_method = fields.Selection(
        related='company_id.datev_export_method',
        readonly=False,
    )
    datev_ignore_currency = fields.Boolean(
        related='company_id.datev_ignore_currency',
        readonly=False,
    )
    l10n_de_datev_client_number = fields.Char(
        related='company_id.l10n_de_datev_client_number',
        readonly=False,
    )
    l10n_de_datev_consultant_number = fields.Char(
        related='company_id.l10n_de_datev_consultant_number',
        readonly=False,
    )
    datev_group_lines = fields.Boolean(
        related='company_id.datev_group_lines',
        readonly=False,
    )
    datev_group_sh = fields.Boolean(
        related='company_id.datev_group_sh',
        readonly=False,
    )
    # endregion
