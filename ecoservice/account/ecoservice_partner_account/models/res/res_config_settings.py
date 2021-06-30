# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # region Fields
    # company_dependent settings explicitly set to readonly=False,
    # otherwise it wouldn't be writeable
    partner_account_generate_automatically = fields.Boolean(
        related='company_id.partner_account_generate_automatically',
        readonly=False,
    )
    partner_account_generate_multi_company = fields.Boolean(
        related='company_id.partner_account_generate_multi_company',
        readonly=False,
    )
    config_set_ref_on_account_creation = fields.Boolean(
        string='Set reference on account creation',
        config_parameter='partner_account.set_ref_on_account_creation',
    )
    partner_account_account_code_ref_preferred = fields.Selection(
        related='company_id.partner_account_account_code_ref_preferred',
        readonly=False,
    )
    # endregion
