# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

import base64
import csv
import io
from datetime import date

from odoo.tests import common


class BaseSetup(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
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
                    'ecoservice_financeinterface: '
                    'Missing dependency "l10n_de_skr03.l10n_de_chart_template". '
                    'Skipping Unit Test...'
                )
            )

        cls.AA = cls.env['account.account']
        cls.ABS = cls.env['account.bank.statement']
        cls.AJ = cls.env['account.journal']
        cls.AM = cls.env['account.move']
        cls.AP = cls.env['account.payment']
        cls.AT = cls.env['account.tax']
        cls.PP = cls.env['product.product']
        cls.RP = cls.env['res.partner'].with_context(
            no_reset_password=True,
            mail_create_nosubscribe=True,
            mail_create_nolog=True,
        )

        cls.customer = cls.RP.create({
            'name': 'Kunde GmbH',
            'email': 'customer@localhost',
            'customer_rank': 1,
        })

        cls.tax_group_19 = cls.env.ref('l10n_de_skr03.tax_group_19')
        cls.tax_group_7 = cls.env.ref('l10n_de_skr03.tax_group_7')
        cls.tax_ust_7 = cls.AT.search(
            [
                ('tax_group_id', '=', cls.tax_group_7.id),
                ('type_tax_use', '=', 'sale'),
            ],
            limit=1,
        )
        cls.tax_ust_19 = cls.AT.search(
            [
                ('tax_group_id', '=', cls.tax_group_19.id),
                ('type_tax_use', '=', 'sale'),
            ],
            limit=1,
        )

        cls.tax_vst_7 = cls.AT.search(
            [
                ('tax_group_id', '=', cls.tax_group_7.id),
                ('type_tax_use', '=', 'purchase'),
            ],
            limit=1,
        )
        cls.tax_vst_19 = cls.AT.search(
            [
                ('tax_group_id', '=', cls.tax_group_19.id),
                ('type_tax_use', '=', 'purchase'),
            ],
            limit=1,
        )
        cls.tax_vst_7_price_include = cls.AT.search(
            [
                ('tax_group_id', '=', cls.tax_group_7.id),
                ('type_tax_use', '=', 'purchase'),
                ('price_include', '=', True)
            ],
            limit=1,
        )
        cls.tax_vst_19_price_include = cls.AT.search(
            [
                ('tax_group_id', '=', cls.tax_group_19.id),
                ('type_tax_use', '=', 'purchase'),
                ('price_include', '=', True)
            ],
            limit=1,
        )

    def _create_invoice(self, invoice_type='out_invoice'):
        return self.AM.create({
            'partner_id': self.customer.id,
            'type': invoice_type,
            'invoice_line_ids': [(0, 0, {
                'name': 'ABC, der Kater lief im Schnee',
                'price_unit': 200.00,
                'quantity': 2,
                'tax_ids': getattr(self, '_tax_' + invoice_type)(),
            })],
        })

    def _tax_in_invoice(self):
        return [
            (6, 0, self.tax_vst_19.ids),
        ]

    def _tax_out_invoice(self):
        return [
            (6, 0, self.tax_ust_19.ids),
        ]

    def _get_csv_reader(self):
        vorlauf = self.env['ecofi'].ecofi_buchungen(
            journal_ids=self.env['account.journal'].search([
                ('company_id', '=', self.env.company.id),
            ]),
            date_from=date.today(),
            date_to=date.today(),
        )

        csv_file = base64.decodebytes(vorlauf.csv_file)
        csv_lines = io.StringIO(csv_file.decode('cp1252'))

        next(csv_lines)
        return csv.DictReader(csv_lines, delimiter=';', quotechar='"')
