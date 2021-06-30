# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # region Fields
    chief_executive_officer = fields.Text()
    report_table_position = fields.Boolean(
        string='Show line item number in printed documents',
        default=True,
    )
    report_table_position_continuous = fields.Boolean(
        string='Share continuous line item numbers across all sections',
        default=True,
    )
    # endregion

    # region Business Methods
    def get_bank_accounts(self):
        if 'account.journal' not in self.env:
            return []
        return self.env['account.journal'].search(
            [
                ('company_id', '=', self.id),
                ('bank_id', '!=', False),
            ],
            limit=4,
        )
    # endregion
