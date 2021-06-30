# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class EcofiValidation(models.Model):
    _name = 'ecofi.validation'
    _description = 'En- or disable specific checks company-wide'

    # region Fields
    company_id = fields.Many2one(
        comodel_name='res.company',
    )
    # account.move.line
    validate_tax_count = fields.Boolean(
        default=True,
        help='Validates that there is max. 1 tax set per line.',
    )
    # endregion

    # region SQL Constraints
    _sql_constraints = [
        (
            'company_unique',
            'unique(company_id)',
            'A configuration for this company already exists!',
        ),
    ]
    # endregion

    def name_get(self):
        return [
            (rec.id, f'Validation Options for {rec.company_id.name}')
            for rec in self
        ]
