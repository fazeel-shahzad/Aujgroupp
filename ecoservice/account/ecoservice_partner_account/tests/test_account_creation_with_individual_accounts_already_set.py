# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup import BaseSetup


class TestAccountCreationWithIndividualAccountsAlreadySet(BaseSetup):

    def setUp(self):
        super().setUp()

        self.partner.create_accounts(['receivable', 'payable'], 'manual')

    def test_create_receivable_account(self):
        partner = self.partner

        partner.action_create_receivable_account()

        self.assertEqual(
            self.sequence_receivable_start,
            partner.property_account_receivable_id.code,
        )
        self.assertEqual(
            self.sequence_payable_start,
            partner.property_account_payable_id.code,
        )

    def test_create_payable_account(self):
        partner = self.partner

        partner.action_create_payable_account()

        self.assertEqual(
            self.sequence_receivable_start,
            partner.property_account_receivable_id.code,
        )
        self.assertEqual(
            self.sequence_payable_start,
            partner.property_account_payable_id.code,
        )

    def test_create_receivable_and_payable_account_simultaneously(self):
        partner = self.partner

        partner.create_accounts(['receivable', 'payable'], 'manual')

        self.assertEqual(
            self.sequence_receivable_start,
            partner.property_account_receivable_id.code,
        )
        self.assertEqual(
            self.sequence_payable_start,
            partner.property_account_payable_id.code,
        )
