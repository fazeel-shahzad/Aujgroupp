# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    def unlink(self):
        accounts = self.sudo()._collect_shared_accounts()

        return super(AccountAccount, accounts).unlink()

    def _collect_shared_accounts(self):
        accounts = self

        shared_companies = self.env['res.company'].search([
            ('partner_account_generate_multi_company', '=', True),
        ])
        shared_accounts = accounts.filtered(
            lambda a: a.company_id in shared_companies,
        )

        if shared_accounts:
            accounts |= accounts.search([
                ('company_id', 'in', shared_companies.ids),
                ('code', 'in', shared_accounts.mapped('code')),
            ])

        return accounts
