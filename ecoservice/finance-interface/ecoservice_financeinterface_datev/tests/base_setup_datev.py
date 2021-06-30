
from odoo.addons.ecoservice_financeinterface.tests.base_setup import BaseSetup

KEY_AMOUNT = 'Umsatz (ohne Soll-/Haben-Kennzeichen)'
KEY_CREDIT_DEBIT = 'Soll-/Haben-Kennzeichen'
KEY_ACCOUNT = 'Konto'
KEY_COUNTER = 'Gegenkonto (ohne BU-Schlüssel)'
KEY_BOOKING_KEY = 'BU-Schlüssel'


class BaseSetupDatev(BaseSetup):

    def setUp(self):
        super(BaseSetupDatev, self).setUp()

        self.env.company.l10n_de_datev_consultant_number = '1234567'
        self.env.company.l10n_de_datev_client_number = 'abcde'

        self.tax_ust_7.l10n_de_datev_code = '2'
        self.tax_ust_19.l10n_de_datev_code = '3'

        (self.tax_vst_7 | self.tax_vst_7_price_include).l10n_de_datev_code = '8'
        (self.tax_vst_19 | self.tax_vst_19_price_include).l10n_de_datev_code = '9'

        self.account_3400 = self.AA.search([
            ('company_id', '=', self.env.company.id),
            ('code', '=', '3400'),
        ])
        self.account_3300 = self.AA.search([
            ('company_id', '=', self.env.company.id),
            ('code', '=', '3300'),
        ])

        self.account_3400.write({
            'datev_tax_ids': [(6, 0, self.tax_vst_19.ids)],
            'datev_automatic_account': True,
        })
        self.account_3300.write({
            'datev_tax_ids': [(6, 0, self.tax_vst_7.ids)],
            'datev_automatic_account': True,
        })

        self.account_8400 = self.AA.search([
            ('company_id', '=', self.env.company.id),
            ('code', '=', '8400'),
        ])
        self.account_8300 = self.AA.search([
            ('company_id', '=', self.env.company.id),
            ('code', '=', '8300'),
        ])
        self.account_8400.write({
            'datev_tax_ids': [(6, 0, self.tax_ust_19.ids)],
            'datev_automatic_account': True,
        })
        self.account_8300.write({
            'datev_tax_ids': [(6, 0, self.tax_ust_7.ids)],
            'datev_automatic_account': True,
        })

    def _test_export_line(self, expected_lines, actual_lines):
        self.assertEqual(
            len(expected_lines),
            len(actual_lines),
        )
        for expected, actual in zip(expected_lines, actual_lines):
            for key in expected:
                self.assertEqual(
                    expected[key],
                    actual[key],
                )
