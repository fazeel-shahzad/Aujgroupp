# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from collections import namedtuple
from typing import List

from .base_setup_datev import BaseSetupDatev

Entry = namedtuple('Entry', ['account', 'debit', 'credit', 'counter'])


class TestCounterAccount(BaseSetupDatev):

    def setUp(self):
        super(TestCounterAccount, self).setUp()

        self.journal = self.AJ.search(
            [
                ('type', '=', 'general'),
                ('company_id', '=', self.env.company.id),
            ],
            limit=1,
        )

    def _account(self, code):
        return self.AA.search(
            args=[
                ('company_id', '=', self.env.company.id),
                ('code', '=', code),
            ],
            limit=1,
        )

    def _create_move_from_entries(self, expected: List[Entry]):
        return self.AM.create({
            'type': 'entry',
            'journal_id': self.journal.id,
            'line_ids': [
                (0, 0, {
                    'account_id': self._account(entry.account).id,
                    'name': 'Stuff',
                    'debit': entry.debit,
                    'credit': entry.credit,
                })
                for entry in expected
            ],
        })

    def _get_actual(self, move):
        return [
            Entry(
                line.account_id.code,
                line.debit,
                line.credit,
                line.ecofi_account_counterpart.code,
            )
            for line in move.line_ids
        ]

    def test_purchase_invoice_counter_account(self):
        invoice = self._create_invoice('in_invoice')

        invoice.set_main_account()

        self.assertEqual(
            self.customer.property_account_payable_id,
            invoice.mapped('line_ids.ecofi_account_counterpart'),
        )

    def test_sales_invoice_counter_account(self):
        invoice = self._create_invoice('out_invoice')

        invoice.set_main_account()

        self.assertEqual(
            self.customer.property_account_receivable_id,
            invoice.mapped('line_ids.ecofi_account_counterpart'),
        )

    # 100: Validations

    # 200: Counter Accounts

    def test_200_single_counter_account_two_lines(self):
        """
        Use the account of the first line as counter account.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('3960', 100.00, 0.00, '3960'),
            Entry('3970', 0.00, 100.00, '3960'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_210_single_counter_account_three_lines(self):
        """
        Use the account of the single debit/credit line as counter account.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('3960', 100.00, 0.00, '3960'),
            Entry('3970', 0.00, 70.00, '3960'),
            Entry('3980', 0.00, 30.00, '3960'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_211_single_counter_account_three_lines_mixed(self):
        """
        Use the account of the single debit/credit line as counter account.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('3970', 0.00, 70.00, '3960'),
            Entry('3960', 100.00, 0.00, '3960'),
            Entry('3980', 0.00, 30.00, '3960'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_212_single_counter_account_two_paires(self):
        """
        Use the account of the first line.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('3960', 100.00, 0.00, '3960'),
            Entry('3970', 0.00, 100.00, '3960'),
            Entry('3960', 200.00, 0.00, '3960'),
            Entry('3970', 0.00, 200.00, '3960'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_220_multiple_counter_accounts_two_transactions(self):
        """
        Use the respective account of the first line of a paired entry.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('0005', 100.00, 0.00, '0005'),
            Entry('0010', 0.00, 100.00, '0005'),

            Entry('0015', 200.00, 0.00, '0015'),
            Entry('0020', 0.00, 200.00, '0015'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_221_multiple_counter_accounts_two_transactions_twisted(self):
        """
        Use the account of the first line of a paired entry.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('0005', 100.00, 0.00, '0005'),
            Entry('0010', 0.00, 100.00, '0005'),

            Entry('0015', 0.00, 200.00, '0015'),
            Entry('0020', 200.00, 0.00, '0015'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_222_multiple_counter_accounts_two_transactions_split(self):
        """
        Use the account of the first line of a paired entry.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('0005', 100.00, 0.00, '0005'),
            Entry('0010', 0.00, 100.00, '0005'),

            Entry('0015', 400.00, 0.00, '0015'),
            Entry('0020', 0.00, 100.00, '0015'),
            Entry('0025', 0.00, 170.00, '0015'),
            Entry('0030', 0.00, 130.00, '0015'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    def test_222_multiple_counter_accounts_two_transactions_split_twisted(self):
        """
        Use the account of the first line of a paired entry.
        """
        expected = [
            # Entry(account, debit, credit, counter)
            Entry('0005', 100.00, 0.00, '0005'),
            Entry('0010', 0.00, 100.00, '0005'),

            Entry('0015', 0.00, 400.00, '0015'),
            Entry('0020', 100.00, 0.00, '0015'),
            Entry('0025', 170.00, 0.00, '0015'),
            Entry('0030', 130.00, 0.00, '0015'),
        ]

        move = self._create_move_from_entries(expected)
        move.set_main_account()

        actual = self._get_actual(move)

        self.assertEqual(expected, actual)

    # 900: ASCII-Exports
