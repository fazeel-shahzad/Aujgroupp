# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import _, api, fields, models


class PartnerAccountConfiguration(models.Model):
    _name = 'partner.account.configuration'
    _description = 'Configuration for each company to generate new accounts.'

    # region Fields
    name = fields.Char(
        string='Description',
        related='company_id.name',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
    )
    account_receivable_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        required=True,
    )
    account_payable_sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        required=True,
    )

    partner_account_generate_automatically = fields.Boolean(
        related='company_id.partner_account_generate_automatically',
        readonly=False,
    )
    partner_account_generate_multi_company = fields.Boolean(
        related='company_id.partner_account_generate_multi_company',
        readonly=False,
    )
    partner_account_account_code_ref_preferred = fields.Selection(
        related='company_id.partner_account_account_code_ref_preferred',
        readonly=False,
    )
    # endregion

    # region Constrains
    _sql_constraints = [
        (
            'code_company_uniq',
            'unique(company_id)',
            _('The configuration must be unique per company!'),
        ),
        (
            'code_receivable_uniq',
            'unique(account_receivable_sequence_id)',
            _('The Receivable Sequence must be unique per configuration!'),
        ),
        (
            'code_payable_uniq',
            'unique(account_payable_sequence_id)',
            _('The Payable Sequence must be unique per configuration!'),
        ),
    ]
    # endregion

    # region Business Methods
    @api.model
    def update_shared_sequences(self) -> None:
        shared = self.with_shared_account_generation()
        for account_type in ['payable', 'receivable']:
            config_sequence_field_name = f'account_{account_type}_sequence_id'

            # set all shared sequences to the highest number_next
            sequences = (
                shared
                .mapped(config_sequence_field_name)
                .sorted(key='number_next_actual', reverse=True)
            )
            if sequences:
                sequences.write({
                    'number_next_actual': sequences[0].number_next_actual,
                })

    @api.model
    def create_accounts_manually(self, partner, account_types: list) -> dict:
        configs = self.for_current_company()

        return configs.create_accounts(partner, account_types)

    @api.model
    def create_accounts_automatically(self, partner, account_types: list) -> dict:
        configs = self.with_automatic_account_generation()

        partner = partner.commercial_partner_id

        return configs.create_accounts(partner, account_types)

    def create_accounts(self, partner, account_types: list) -> dict:
        update_shared = False
        configs = self

        if any(c.partner_account_generate_multi_company for c in configs):
            update_shared = True
            configs |= self.with_shared_account_generation()

        accounts = configs.sudo()._create_accounts(partner, account_types)

        if update_shared:
            self.update_shared_sequences()

        return accounts

    def _create_accounts(self, partner, account_types: list) -> dict:
        accounts_of_current_company = {}
        current_company = self.current_company()

        for account_type in account_types:
            field = f'property_account_{account_type}_id'

            for config in self:
                if not self._is_default_account(
                    partner,
                    config.company_id,
                    account_type,
                ):
                    continue
                account = config._create_account(partner, account_type)
                setattr(
                    partner.with_context(
                        force_company=config.company_id.id,
                    ),
                    field,
                    account,
                )
                if config.company_id == current_company:
                    accounts_of_current_company[account_type] = account.code
        return accounts_of_current_company

    @api.model
    def _is_default_account(self, partner, company, account_type: str) -> bool:
        partner_com = partner.with_context(force_company=company.id)
        default_field = f'property_account_{account_type}_is_default'

        return getattr(partner_com, default_field)

    def _create_account(self, partner, account_type: str, code: str = None):
        self.ensure_one()

        if not code:
            code = self._account_code(account_type)

        return self.env['account.account'].create({
            'company_id':
                self.company_id.id,
            'currency_id':
                self.company_id.currency_id.id,
            'code':
                code,
            'name':
                partner.commercial_partner_id.name,
            'reconcile':
                True,
            'user_type_id': self.env.ref(
                f'account.data_account_type_{account_type}',
            ).id,
        })

    def _account_code(self, account_type: str) -> str:
        return getattr(self, f'account_{account_type}_sequence_id').next_by_id()

    @api.model
    def with_automatic_account_generation(self):
        return self.sudo().search([
            ('partner_account_generate_automatically', '=', True),
        ])

    @api.model
    def with_shared_account_generation(self):
        return self.sudo().search([
            ('partner_account_generate_multi_company', '=', True),
        ])

    @api.model
    def for_current_company(self):
        return self.sudo().search(
            [
                ('company_id', '=', self.sudo().current_company().id),
            ],
            limit=1,
        )

    @api.model
    def current_company(self):
        company = self.env.context.get('force_company')
        if company:
            return self.env['res.company'].browse(company)
        return self.env.company
    # endregion
