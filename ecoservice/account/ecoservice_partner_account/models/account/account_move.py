# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def post(self) -> None:
        self._create_and_update_accounts()

        return super(AccountMove, self).post()

    def _create_and_update_accounts(self):
        for move in self:
            if move.type.startswith('out_'):
                account_type = 'receivable'
            elif move.type.startswith('in_'):
                account_type = 'payable'
            else:
                continue

            account = move._create_account(account_type)
            move._update_account(account, account_type)

    def _create_account(self, account_type: str):
        partner = self._partner_with_company()
        field = f'property_account_{account_type}_id'

        partner.create_accounts([account_type], 'auto')

        return getattr(partner, field)

    def _update_account(self, account, account_type: str) -> None:
        lines_to_update = self.line_ids.filtered(
            lambda l: l.account_internal_type == account_type,
        )
        lines_to_update.account_id = account

    def _partner_with_company(self):
        return self.with_context(force_company=self.company_id.id).partner_id
