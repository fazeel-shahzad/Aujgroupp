# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


# noinspection PyAttributeOutsideInit,PyTypeChecker
class ResPartner(models.Model):
    _inherit = 'res.partner'

    # region Fields
    property_account_payable_is_default = fields.Boolean(
        compute='_compute_account_is_default',
        compute_sudo=True,
    )
    property_account_receivable_is_default = fields.Boolean(
        compute='_compute_account_is_default',
        compute_sudo=True,
    )
    # endregion

    # region Compute Methods
    @api.depends(
        'property_account_payable_id',
        'property_account_receivable_id',
    )
    @api.depends_context(
        'force_company',
    )
    def _compute_account_is_default(self):
        payable = 'property_account_payable_id'
        receivable = 'property_account_receivable_id'
        defaults = self.default_get([payable, receivable])

        for partner in self:
            partner.property_account_payable_is_default = (
                defaults[payable] == partner[payable].id
            )
            partner.property_account_receivable_is_default = (
                defaults[receivable] == partner[receivable].id
            )
    # endregion

    # region CRUD Methods
    @api.model_create_single
    def create(self, values: dict):
        partner = super(ResPartner, self).create(values)

        account_types = []

        if values.get('customer_rank'):
            account_types.append('receivable')
        if values.get('supplier_rank'):
            account_types.append('payable')

        partner.create_accounts(account_types, 'auto')

        return partner
    # endregion

    # region Action Methods
    def action_create_payable_account(self) -> bool:
        """
        Create a payable account from the GUI.

        Creating an account from the GUI always counts as manual creation.
        Thus any automatic account creation setting is ignored. The sharing
        setting is taken into account though.
        """
        self.ensure_one()

        if not self.property_account_payable_is_default:
            return True

        self.create_accounts(['payable'], 'manual')

        return True

    def action_create_receivable_account(self) -> bool:
        """
        Create a receivable account from the GUI.

        Creating an account from the GUI always counts as manual creation.
        Thus any automatic account creation setting is ignored. The sharing
        setting is taken into account though.
        """
        self.ensure_one()

        if not self.property_account_receivable_is_default:
            return True

        self.create_accounts(['receivable'], 'manual')

        return True
    # endregion

    # region Business Methods
    def create_accounts(self, account_types: list, creation_mode: str) -> bool:
        config = self.env['partner.account.configuration'].sudo()
        set_ref = self.env['ir.config_parameter'].sudo().get_param(
            'partner_account.set_ref_on_account_creation',
        )

        if creation_mode == 'manual':
            creation_method = config.create_accounts_manually
        elif creation_mode == 'auto':
            creation_method = config.create_accounts_automatically
        else:
            raise UserError(_(
                "creation_mode must be either 'manual' or 'auto'!",
            ))

        for partner in self:
            accounts = creation_method(partner, account_types)
            if set_ref:
                partner.set_ref(accounts)

        return True

    def set_ref(self, accounts: dict) -> None:
        self.ensure_one()

        # Don't overwrite an already set ref!
        if self.ref:
            return

        if accounts.get('payable') and accounts.get('receivable'):
            self.ref = accounts[
                self.env.company.partner_account_account_code_ref_preferred
            ]
        elif accounts.get('receivable'):
            self.ref = accounts['receivable']
        elif accounts.get('payable'):
            self.ref = accounts['payable']
    # endregion
