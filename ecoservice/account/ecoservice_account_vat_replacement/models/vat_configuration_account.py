# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class VatConfigurationAccount(models.Model):
    _name = 'vat.configuration.account'
    _description = 'VAT Configuration Account Line'

    # region Fields
    configuration_id = fields.Many2one(
        comodel_name='vat.configuration',
        required=True,
        ondelete='cascade',
    )

    source_account_id = fields.Many2one(
        comodel_name='account.account',
        required=True,
    )
    target_account_id = fields.Many2one(
        comodel_name='account.account',
        required=True,
    )
    # endregion

    # region Constrains
    _sql_constraints = [
        (
            'unique_source_account',
            'unique(configuration_id, source_account_id)',
            'You must not replace the source account more than once'
            ' within one configuration!',
        )
    ]
    # endregion
