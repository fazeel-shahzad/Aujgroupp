# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    datev_cashback_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Datev Cashback Account',
    )
