# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class EcoserviceFinanceInterfaceConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # region Fields
    # no default prefix as this will break in multi-company (see task #12442)
    journal_ids = fields.Many2many(
        related='company_id.journal_ids',
        readonly=False,
    )
    default_ecofi_validations_enabled = fields.Boolean(
        default_model='account.move',
        related='company_id.ecofi_validations_enabled',
        readonly=False,
    )
    ecofi_validation_id = fields.Many2one(
        related='company_id.ecofi_validation_id',
        readonly=True,
    )
    # endregion
