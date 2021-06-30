# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup import BaseSetup


class TestConfigGeneration(BaseSetup):

    def test_configuration_generation_install(self):
        """
        Configuration should be created directly after install.
        """
        company = self.env.company

        self._test_configuration(company)

    def test_configuration_generation_create(self):
        company = self.RC.create({
            'name': 'Company Config',
            'chart_template_id': self.account_chart.id,
        })

        self._test_configuration(company)

    def _test_configuration(self, company):
        config = self.PAC.search([('company_id', '=', company.id)], limit=1)

        self.assertTrue(
            bool(config),
        )
        self.assertEqual(
            company,
            config.company_id,
        )
        self.assertEqual(
            company,
            config.account_receivable_sequence_id.company_id,
        )
        self.assertEqual(
            company,
            config.account_payable_sequence_id.company_id,
        )
