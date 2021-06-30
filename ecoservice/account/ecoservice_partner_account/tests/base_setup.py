# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo.tests.common import SavepointCase


class BaseSetup(SavepointCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # Check dependencies before doing anything else.
        cls.account_chart = cls.env.ref(
            'l10n_de_skr03.l10n_de_chart_template',
            raise_if_not_found=False,
        )
        if not cls.account_chart:
            cls.skipTest(
                cls,
                reason=(
                    'ecoservice_partner_account: '
                    'Missing dependency "l10n_de_skr03.l10n_de_chart_template". '
                    'Skipping Unit Test...'
                )
            )

        cls.AA = cls.env['account.account']
        cls.ACT = cls.env['account.chart.template']
        cls.AJ = cls.env['account.journal']
        cls.AM = cls.env['account.move']
        cls.PAC = cls.env['partner.account.configuration']
        cls.RC = cls.env['res.company']
        cls.RP = cls.env['res.partner'].with_context(
            no_reset_password=True,
            mail_create_nosubscribe=True,
            mail_create_nolog=True,
        )
        cls.RU = cls.env['res.users'].with_context(
            no_reset_password=True,
            mail_create_nosubscribe=True,
        )

        cls.partner = cls.RP.create({
            'name': 'Hans Dampf',
            'is_company': False,
        })

        cls.account_receivable = cls.account_chart.property_account_payable_id
        cls.account_payable = cls.account_chart.property_account_receivable_id

        # We make sure to start late in order to not run into problems
        # when the tests are run on an already populated database
        cls.sequence_payable_start = '90000'  # SKR payables 70000 - 99999
        cls.sequence_receivable_start = '60000'  # SKR receivables 10000 - 69999

        cls.company_1 = cls.env.company

        # make sure all the default settings are set
        cls.company_1.write({
            'partner_account_generate_automatically': False,
            'partner_account_generate_multi_company': False,
            'partner_account_account_code_ref_preferred': 'receivable',
        })

    def setUp(self):
        super().setUp()

        pac = self.PAC.sudo().search([])

        pac.account_receivable_sequence_id.number_next_actual = int(
            self.sequence_receivable_start,
        )
        pac.account_payable_sequence_id.number_next_actual = int(
            self.sequence_payable_start,
        )

        self._disable_ref()

    def _enable_ref(self):
        self.env['ir.config_parameter'].set_param(
            'partner_account.set_ref_on_account_creation',
            True,
        )

    def _disable_ref(self):
        self.env['ir.config_parameter'].set_param(
            'partner_account.set_ref_on_account_creation',
            False,
        )
