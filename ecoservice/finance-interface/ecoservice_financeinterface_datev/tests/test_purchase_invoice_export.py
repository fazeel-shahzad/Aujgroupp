# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from .base_setup_datev import (
    KEY_ACCOUNT,
    KEY_AMOUNT,
    KEY_BOOKING_KEY,
    KEY_COUNTER,
    KEY_CREDIT_DEBIT,
    BaseSetupDatev,
)


class TestPurchaseInvoiceExport(BaseSetupDatev):

    def setUp(self):
        super().setUp()

        self.account_4210 = self.AA.search([
            ('company_id', '=', self.env.company.id),
            ('code', '=', '4210'),
        ])

        self.invoice = self.AM.create({
            'partner_id': self.customer.id,
            'type': 'in_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'ABC',
                    'account_id': self.account_3400.id,
                    'price_unit': 200.00,
                    'quantity': 2,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
                (0, 0, {
                    'name': 'DEF',
                    'account_id': self.account_3300.id,
                    'price_unit': 400.00,
                    'quantity': 3,
                    'tax_ids': [
                        (6, 0, self.tax_vst_7.ids),
                    ],
                }),
            ],
        })

    def test_00_invoice_export_simple(self):
        # This test should be independent of configurations
        expected_lines = [{
            KEY_AMOUNT: '476,00',
            KEY_CREDIT_DEBIT: 'S',
            KEY_ACCOUNT: '3400',
            KEY_COUNTER: '1610',
            KEY_BOOKING_KEY: '',
        }]

        invoice = self._create_invoice('in_invoice')
        invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # Test 1
    # Konfiguration:
    # Buchungszeilen gruppieren: nein
    # Soll und Haben kumulieren: nein
    # Geschäftsfall: Ausgangsrechnung 2 Positionen

    # TODO Ob Ergebnis so sein soll, auf Ausgang der Diskussion im ecoFI-Kanal warten
    # Gegenkonto aus dem Partner
    # 8400 wird nicht zusammengefasst
    # Soll-/Haben-K: h

    def test_invoice_export_no_group_line_no_accumulate_debit_credit(self):
        self.env.company.write({
            'datev_group_lines': False,
            'datev_group_sh': False,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '476,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3400',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
            {
                KEY_AMOUNT: '1284,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3300',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
        ]

        self.invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # Test 2
    # Konfiguration:
    # Buchungszeilen gruppieren: ja
    # Soll und Haben kumulieren: nein
    # Geschäftsfall: Ausgangsrechnung 2 Positionen

    # TODO Ob Ergebnis so sein, auf Ausgang der Diskussion im ecoFI-Kanal warten
    # Gegenkonto aus dem Partner
    # 8400 wird zusammengefasst / Pos. 1 und 2. gleiches Konto & Steuer gleich
    # Soll-/Haben-K: h

    def test_invoice_export_yes_group_line_no_accumulate_debit_credit(self):
        self.env.company.write({
            'datev_group_lines': True,
            'datev_group_sh': False,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '595,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3400',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
            {
                KEY_AMOUNT: '1284,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3300',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
        ]

        self.invoice.write({
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'ABC2',
                    'account_id': self.account_3400.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
            ],
        })
        # Odoo changes the accounts of all lines to 3400
        # after adding the 3rd line. Therefore we need to reset it to 3300.
        self.invoice.write({
            'invoice_line_ids': [
                (1, self.invoice.invoice_line_ids[1].id, {
                    'account_id': self.account_3300.id
                }),
            ],
        })
        self.invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # Test 3 (falsch)
    # Konfiguration:
    # Buchungszeilen gruppieren: ja
    # Soll und Haben kumulieren: nein
    # Geschäftsfall: Ausgangsrechnung 2 Positionen und eine Rabatt-Position

    # TODO Ob Ergebnis so sein, auf Ausgang der Diskussion im ecoFI-Kanal warten
    # Konto und Gegenkonto sind gedreht (Gegenkonto müsste vom Partner gezogen werden)
    # 8400 nicht zusammengefasst (müsste zusammengefasst werden)
    # Soll-/Haben-K: falsch (Rabattzeile dürfte nicht zusammengefasst werden, Konf. Haken bei nicht kummulieren)

    def test_invoice_export_yes_group_line_no_accumulate_debit_credit_discount(self):
        self.env.company.write({
            'datev_group_lines': True,
            'datev_group_sh': False,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '595,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3400',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
            {
                KEY_AMOUNT: '1284,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3300',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
            {
                KEY_AMOUNT: '119,00',
                KEY_CREDIT_DEBIT: 'H',
                KEY_ACCOUNT: '3400',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
        ]

        self.invoice.write({
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'ABC2',
                    'account_id': self.account_3400.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
                (0, 0, {
                    'name': 'Discount',
                    'account_id': self.account_3400.id,
                    'price_unit': -100.00,  # discount line
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
            ],
        })
        # Odoo changes the accounts of all lines to 3400
        # after adding the 3rd line. Therefore we need to reset it to 3300.
        self.invoice.invoice_line_ids[1].account_id = self.account_3300
        self.invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # Test 4
    # Konfiguration:
    # Buchungszeilen gruppieren: ja
    # Soll und Haben kumulieren: ja
    # Geschäftsfall: Ausgangsrechnung 2 Positionen und eine Rabatt-Position

    # TODO Ob Ergebnis so sein, auf Ausgang der Diskussion im ecoFI-Kanal warten
    # Gegenkonto aus dem Partner
    # 8400 wird zusammengefasst / Pos. 1 und 2. gleiches Konto & Steuer gleich
    # Die Rabattzeile wurde mit Konto 8400 kumuliert

    # TODO: for now just copied from tests above. needs correct test
    def test_invoice_export_yes_group_line_yes_accumulate_debit_credit_discount(self):
        self.env.company.write({
            'datev_group_lines': True,
            'datev_group_sh': True,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '476,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3400',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
            {
                KEY_AMOUNT: '1284,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '3300',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
        ]

        self.invoice.write({
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'ABC2',
                    'account_id': self.account_3400.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
                (0, 0, {
                    'name': 'Discount',
                    'account_id': self.account_3400.id,
                    'price_unit': -100.00,
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
            ],
        })
        # Odoo changes the accounts of all lines to 3400
        # after adding the 3rd line. Therefore we need to reset it to 3300.
        self.invoice.invoice_line_ids[1].account_id = self.account_3300
        self.invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # Test 7
    # Konfiguration:
    # Buchungszeilen gruppieren: ja
    # Soll und Haben kumulieren: ja
    # Geschäftsfall: Eine Eingangsrechnung mit einem Konto, welches nicht Automatikkonto ist.
    #                Die Vorsteuer wurde auf inklusive Steuer gesetzt.

    # Gegenkonto aus dem Partner
    # Konto ist kein Automatikkonto
    # Vorsteuer ist inkl. Steuer

    def test_invoice_export_yes_group_line_yes_accumulate_no_auto_account(self):
        self.env.company.write({
            'datev_group_lines': True,
            'datev_group_sh': True,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '119,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '4210',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '9',
            },
        ]

        invoice = self.AM.create({
            'partner_id': self.customer.id,
            'type': 'in_invoice',
            'invoice_line_ids': [(0, 0, {
                'name': 'ABC, der Kater lief im Schnee',
                'account_id': self.account_4210.id,
                'price_unit': 119.00,
                'quantity': 1,
                'tax_ids': [
                        (6, 0, self.tax_vst_19_price_include.ids),
                    ],
            })],
        })

        invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # see #12354
    def test_grouping_with_taking_tax_into_account(self):
        self.env.company.write({
            'datev_group_lines': True,
            'datev_group_sh': False,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '119,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '4210',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '9',
            },
            {
                KEY_AMOUNT: '100,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '4210',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
        ]

        invoice = self.AM.create({
            'partner_id': self.customer.id,
            'type': 'in_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Miete',
                    'account_id': self.account_4210.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
                (0, 0, {
                    'name': 'Miete',
                    'account_id': self.account_4210.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                }),
            ],
        })

        invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    # see #12354
    def test_grouping_combined_with_taking_tax_into_account(self):
        self.env.company.write({
            'datev_group_lines': True,
            'datev_group_sh': True,
        })

        expected_lines = [
            {
                KEY_AMOUNT: '119,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '4210',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '9',
            },
            {
                KEY_AMOUNT: '100,00',
                KEY_CREDIT_DEBIT: 'S',
                KEY_ACCOUNT: '4210',
                KEY_COUNTER: '1610',
                KEY_BOOKING_KEY: '',
            },
        ]

        invoice = self.AM.create({
            'partner_id': self.customer.id,
            'type': 'in_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Miete',
                    'account_id': self.account_4210.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                    'tax_ids': [
                        (6, 0, self.tax_vst_19.ids),
                    ],
                }),
                (0, 0, {
                    'name': 'Miete',
                    'account_id': self.account_4210.id,
                    'price_unit': 100.00,
                    'quantity': 1,
                }),
            ],
        })

        invoice.post()

        actual_lines = list(self._get_csv_reader())

        self._test_export_line(expected_lines, actual_lines)

    def test_invoice_export_currency(self):
        self.skipTest('TODO: Klären')
