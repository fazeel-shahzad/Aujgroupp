# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class VatConfigurationTax(models.Model):
    _name = 'vat.configuration.tax'
    _description = 'VAT Configuration Tax Line'

    # region Fields
    configuration_id = fields.Many2one(
        comodel_name='vat.configuration',
        required=True,
        ondelete='cascade',
    )

    source_tax_id = fields.Many2one(
        comodel_name='account.tax',
        required=True,
    )
    target_tax_id = fields.Many2one(
        comodel_name='account.tax',
        required=True,
    )
    # endregion

    # region Constrains
    _sql_constraints = [
        (
            'unique_source_tax',
            'unique(configuration_id, source_tax_id)',
            'You must not replace the source tax more than once'
            ' within one configuration!',
        )
    ]
    # endregion
