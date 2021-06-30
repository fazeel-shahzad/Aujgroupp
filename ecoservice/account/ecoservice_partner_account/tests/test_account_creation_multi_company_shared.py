# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo.exceptions import UserError

from .base_setup_multi_company import BaseSetupMultiCompany


# noinspection DuplicatedCode
class TestAccountCreationMultiCompanyShared(BaseSetupMultiCompany):

    def setUp(self):
        super().setUp()

        pac2 = self.PAC.sudo().search([('company_id', '=', self.company_2.id)])
        pac3 = self.PAC.sudo().search([('company_id', '=', self.company_3.id)])

        self.csr_2 = str(
            int(self.sequence_receivable_start) + 2
        )
        self.csp_2 = str(
            int(self.sequence_payable_start) + 2
        )
        self.csr_3 = str(
            int(self.sequence_receivable_start) + 3
        )
        self.csp_3 = str(
            int(self.sequence_payable_start) + 3
        )

        pac2.account_receivable_sequence_id.number_next_actual = int(self.csr_2)
        pac2.account_payable_sequence_id.number_next_actual = int(self.csp_2)

        pac3.account_receivable_sequence_id.number_next_actual = int(self.csr_3)
        pac3.account_payable_sequence_id.number_next_actual = int(self.csp_3)

        (self.company_1 | self.company_2).write({
            'partner_account_generate_multi_company': True,
        })

    def test_00_config_check(self):
        pac1 = self.PAC.sudo().search([('company_id', '=', self.company_1.id)])
        pac2 = self.PAC.sudo().search([('company_id', '=', self.company_2.id)])
        pac3 = self.PAC.sudo().search([('company_id', '=', self.company_3.id)])

        self.assertEqual(
            int(self.sequence_receivable_start) + 2,
            pac1.account_receivable_sequence_id.number_next_actual,
        )
        self.assertEqual(
            int(self.sequence_payable_start) + 2,
            pac1.account_payable_sequence_id.number_next_actual,
        )

        self.assertEqual(
            int(self.sequence_receivable_start) + 2,
            pac2.account_receivable_sequence_id.number_next_actual,
        )
        self.assertEqual(
            int(self.sequence_payable_start) + 2,
            pac2.account_payable_sequence_id.number_next_actual,
        )

        self.assertEqual(
            int(self.sequence_receivable_start) + 3,
            pac3.account_receivable_sequence_id.number_next_actual,
        )
        self.assertEqual(
            int(self.sequence_payable_start) + 3,
            pac3.account_payable_sequence_id.number_next_actual,
        )

    def test_create_receivable_account(self):
        # Arrange
        partner = self.partner

        # Act
        partner.action_create_receivable_account()

        # Assert
        # Company 1
        self.assertFalse(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_receivable_start) + 2),
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_id.code,
        )

        # Company 2
        self.assertFalse(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_receivable_start) + 2),
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_id.code,
        )

    def test_create_payable_account(self):
        # Arrange
        partner = self.partner

        # Act
        partner.action_create_payable_account()

        # Assert
        # Company 1
        self.assertTrue(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_is_default,
        )
        self.assertFalse(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_payable_start) + 2),
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_id.code,
        )

        # Company 2
        self.assertFalse(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_payable_start) + 2),
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_id.code,
        )

    def test_create_receivable_and_payable_account_simultaneously(self):
        # Arrange
        partner = self.partner

        # Act
        partner.create_accounts(['receivable', 'payable'], 'manual')

        # Assert
        # Company 1
        self.assertFalse(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_is_default,
        )
        self.assertFalse(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_payable_start) + 2),
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_id.code,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_receivable_start) + 2),
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_id.code,
        )

        # Company 2
        self.assertFalse(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_is_default,
        )
        self.assertFalse(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_is_default,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_payable_start) + 2),
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_id.code,
        )
        self.assertEqual(
            partner.name,
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_id.name,
        )
        self.assertEqual(
            str(int(self.sequence_receivable_start) + 2),
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_id.code,
        )

    def test_create_receivable_account_unshared_is_still_default(self):
        # Arrange
        partner = self.partner

        # Act
        partner.action_create_receivable_account()

        # Assert
        self.assertTrue(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_payable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_receivable_is_default,
        )

    def test_create_payable_account_unshared_is_still_default(self):
        # Arrange
        partner = self.partner

        # Act
        partner.action_create_payable_account()

        # Assert
        self.assertTrue(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_payable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_receivable_is_default,
        )

    def test_create_receivable_and_payable_account_simultaneously_unshared_is_still_default(self):
        # Arrange
        partner = self.partner

        # Act
        partner.create_accounts(['receivable', 'payable'], 'manual')

        # Assert
        self.assertTrue(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_payable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_receivable_is_default,
        )

    def test_create_receivable_and_payable_for_unshared_other_remain_default(self):
        # Arrange
        partner = self.partner.with_context(force_company=self.company_3.id)

        # Act
        partner.create_accounts(['receivable', 'payable'], 'manual')

        # Assert
        self.assertTrue(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_payable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_1.id,
            ).property_account_receivable_is_default,
        )

        self.assertTrue(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_payable_is_default,
        )
        self.assertTrue(
            partner.with_context(
                force_company=self.company_2.id,
            ).property_account_receivable_is_default,
        )

        self.assertFalse(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_payable_is_default,
        )
        self.assertFalse(
            partner.with_context(
                force_company=self.company_3.id,
            ).property_account_receivable_is_default,
        )

    def test_multiple_account_deletion(self):
        # Arrange
        partner = self.partner
        partner.create_accounts(['receivable', 'payable'], 'manual')
        account = partner.property_account_receivable_id
        account_code = account.code

        # Act
        # Somehow setting the field to false doesn't work for the second company
        self.env['ir.property'].search([
            ('name', '=', 'property_account_receivable_id'),
            ('res_id', '=', f'res.partner,{partner.id}'),
        ]).unlink()

        account.unlink()

        # Assert
        self.assertFalse(
            self.AA.sudo().search([
                ('code', '=', account_code),
            ])
        )

    def test_multiple_account_deletion_fails(self):
        # Arrange
        partner = self.partner

        # Act
        partner.create_accounts(['receivable', 'payable'], 'manual')

        # Assert
        with self.assertRaises(UserError):
            partner.property_account_receivable_id.unlink()
