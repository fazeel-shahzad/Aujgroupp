# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import exceptions

from .base_setup import BaseSetup


class TestTaxCount(BaseSetup):

    def test_line_without_tax(self):
        try:
            invoice = self.AM.create({
                'partner_id': self.customer.id,
                'type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'name': 'DEF, ?',
                    'price_unit': 200.00,
                    'quantity': 2,
                })],
            })
        except Exception as e:
            self.fail('Unexpected exception was raised: {}'.format(e))

    def test_line_with_one_tax(self):
        try:
            invoice = self.AM.create({
                'partner_id': self.customer.id,
                'type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'name': 'DEF, ?',
                    'price_unit': 200.00,
                    'quantity': 2,
                    'tax_ids': [
                        (6, 0, self.tax_ust_19.ids),
                    ],
                })],
            })
        except Exception as e:
            self.fail('Unexpected exception was raised: {}'.format(e))

    def test_line_with_more_than_one_tax(self):
        with self.assertRaises(exceptions.ValidationError):
            invoice = self.AM.create({
                'partner_id': self.customer.id,
                'type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'name': 'DEF, ?',
                    'price_unit': 200.00,
                    'quantity': 2,
                    'tax_ids': [
                        (6, 0, (self.tax_ust_7 + self.tax_ust_19).ids),
                    ],
                })],
            })
