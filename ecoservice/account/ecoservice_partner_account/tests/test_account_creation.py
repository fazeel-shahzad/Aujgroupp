# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup import BaseSetup


class TestAccountCreation(BaseSetup):

    def test_create_receivable_account(self):
        # Arrange
        partner = self.partner

        # Act
        partner.action_create_receivable_account()

        # Assert
        self.assertFalse(
            partner.property_account_receivable_is_default,
        )
        self.assertTrue(
            partner.property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.property_account_receivable_id.name,
        )
        self.assertEqual(
            self.sequence_receivable_start,
            partner.property_account_receivable_id.code,
        )

    def test_create_payable_account(self):
        partner = self.partner

        partner.action_create_payable_account()

        self.assertTrue(
            partner.property_account_receivable_is_default,
        )
        self.assertFalse(
            partner.property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.property_account_payable_id.name,
        )
        self.assertEqual(
            self.sequence_payable_start,
            partner.property_account_payable_id.code,
        )

    def test_create_receivable_and_payable_account_simultaneously(self):
        partner = self.partner

        partner.create_accounts(['receivable', 'payable'], 'manual')

        self.assertFalse(
            partner.property_account_receivable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.property_account_receivable_id.name,
        )
        self.assertEqual(
            self.sequence_receivable_start,
            partner.property_account_receivable_id.code,
        )

        self.assertFalse(
            partner.property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.property_account_payable_id.name,
        )
        self.assertEqual(
            self.sequence_payable_start,
            partner.property_account_payable_id.code,
        )

    def test_create_account_with_standard_user(self):
        user = self.RU.create([{
            'name': 'Donald Durchschnittlich',
            'login': 'dd',
        }])

        self.RP.with_user(user).create({
            'name': 'Some Company',
        })
