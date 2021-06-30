# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    def is_tax_account(self) -> bool:
        """
        Check if the selected account is a tax account.
        """
        self.ensure_one()
        repartition = self.env['account.tax.repartition.line'].search(
            [('account_id', '=', self.id)],
        )
        return bool(repartition)
