# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup import BaseSetup


class TestAccountCreationWithReferenceSettingAndReferenceAlreadySet(BaseSetup):

    def setUp(self):
        super().setUp()

        self.partner.ref = 'Might be Batman'

    def test_create_receivable_account(self):
        partner = self.partner
        ref = partner.ref

        partner.action_create_receivable_account()

        self.assertEqual(
            ref,
            partner.ref,
        )

    def test_create_payable_account(self):
        partner = self.partner
        ref = partner.ref

        partner.action_create_payable_account()

        self.assertEqual(
            ref,
            partner.ref,
        )

    def test_create_receivable_and_payable_account_simultaneously_customer_preferred(self):
        self.env.company.partner_account_account_code_ref_preferred = 'receivable'
        partner = self.partner
        ref = partner.ref

        partner.create_accounts(['receivable', 'payable'], 'manual')

        self.assertEqual(
            ref,
            partner.ref,
        )

    def test_create_receivable_and_payable_account_simultaneously_supplier_preferred(self):
        self.env.company.partner_account_account_code_ref_preferred = 'payable'
        partner = self.partner
        ref = partner.ref

        partner.create_accounts(['receivable', 'payable'], 'manual')

        self.assertEqual(
            ref,
            partner.ref,
        )
