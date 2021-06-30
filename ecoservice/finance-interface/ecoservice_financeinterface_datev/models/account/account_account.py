# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import _, api, exceptions, fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    # region Fields
    datev_vat_handover = fields.Boolean(
        string='Datev VAT-ID',
        help='Is required when transferring a sales tax identification number'
             ' from the account partner (e.g. EU-Invoice)',
    )
    datev_automatic_account = fields.Boolean()
    datev_tax_ids = fields.Many2many(
        comodel_name='account.tax',
        relation='account_tax_rel',
        column1='account_id',
        column2='tax_id',
        string='Datev Tax Account',
        domain=[('l10n_de_datev_code', '!=', '')],
    )
    datev_tax_required = fields.Boolean(
        string='Tax posting required?',
    )
    # endregion

    # region Constraints
    @api.constrains('datev_tax_ids')
    def _check_auto_account_datev_tax_ids(self):
        for account in self.filtered('datev_automatic_account'):
            if not account.datev_tax_ids:
                raise exceptions.ValidationError(
                    _(
                        'There must be at least 1 DATEV tax account '
                        'if you want to mark this account as automatic account!'
                    )
                )
    # endregion
