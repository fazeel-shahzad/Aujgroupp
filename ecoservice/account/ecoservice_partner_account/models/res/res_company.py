# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # region Fields
    partner_account_generate_automatically = fields.Boolean(
        string='Automatic Account Generation',
    )
    partner_account_generate_multi_company = fields.Boolean(
        string='Share Accounts',
    )
    partner_account_account_code_ref_preferred = fields.Selection(
        selection=[
            ('receivable', 'Customer'),
            ('payable', 'Supplier'),
        ],
        string='Preferred Account',
        default='receivable',
    )
    # endregion

    # region CRUD Methods
    @api.model
    def create(self, values):
        company = super().create(values)
        company.create_partner_account_configuration()
        return company

    def write(self, values):
        result = super().write(values)
        self.create_partner_account_configuration()
        # Update shared after possible creation of configuration
        if 'partner_account_generate_multi_company' in values:
            self.env['partner.account.configuration'].update_shared_sequences()
        return result
    # endregion

    # region Business Methods
    def create_partner_account_configuration(self):
        """
        Create a configuration per company.
        """
        companies = self._need_account_configuration()
        values = companies._create_partner_account_configuration_values()

        return self.env['partner.account.configuration'].create(values)

    def _need_account_configuration(self):
        companies = self.filtered('chart_template_id')

        if not companies:
            return companies

        configurations = self.env['partner.account.configuration'].read_group(
            [('company_id', 'in', companies.ids)],
            ['company_id'],
            ['company_id'],
        )
        configurations = [
            company['company_id'][0]
            for company
            in configurations
        ]

        return companies.filtered(
            lambda c: c.id not in configurations,
        )

    def _create_partner_account_configuration_values(self):
        values = []

        account_receivable_type = self.env.ref(
            'account.data_account_type_receivable',
        )
        account_payable_type = self.env.ref(
            'account.data_account_type_payable',
        )

        for company in self:
            account_receivable_sequence = company.create_account_sequence(
                account_receivable_type,
            )
            account_payable_sequence = company.create_account_sequence(
                account_payable_type,
            )

            # actual configuration
            values.append({
                'company_id':
                    company.id,
                'account_receivable_sequence_id':
                    account_receivable_sequence.id,
                'account_payable_sequence_id':
                    account_payable_sequence.id,
            })

        return values

    def create_account_sequence(self, account_type):
        """
        Create a new sequence to generate new account codes with it.

        Will automatically set the padding and next number depending on
        the chart of account of the company.
        The next number will be set to the highest account code + 1
        if the codes are digits only.

        :param account_type: Type of the account this sequence is for
        :return: Created sequence
        """
        self.ensure_one()

        return self.env['ir.sequence'].create(
            self._create_account_generation_sequence_values(account_type),
        )

    def _create_account_generation_sequence_values(self, account_type):
        account_chart_code_digits = self.chart_template_id.code_digits + 1

        params = {
            'account_chart_code_digits': account_chart_code_digits,
            'account_type': account_type.id,
            'company': self.id,
        }
        number_next = self._get_number_next(params)

        return {
            'code':
                'ecoservice.partner.account.{type}'.format_map(account_type),
            'company_id':
                self.id,
            'name':
                f'{account_type.name}: {self.name}',
            'number_next':
                number_next or self._default_account_codes()[account_type.type],
            'padding':
                account_chart_code_digits,
        }

    @api.model
    def _default_account_codes(self) -> dict:
        return {
            'payable': 70000,
            'receivable': 10000,
        }

    def _get_number_next(self, params: dict):
        """
        Search the highest account code.

        :type params: dict
        :param params: Parameter necessary to find the highest account code
        :rtype: int|bool
        :return: Highest account code+1 if code is digit only otherwise False
        """

        query = """
            SELECT code
            FROM account_account
            WHERE user_type_id = %(account_type)s
            AND LENGTH(code) = %(account_chart_code_digits)s
            AND company_id = %(company)s
            ORDER BY code DESC
            LIMIT 1
        """
        self.env.cr.execute(query, params=params)
        result = self.env.cr.dictfetchone()
        return (
            result
            and result.get('code', '').isdigit()
            and int(result['code']) + 1
        )
    # endregion
