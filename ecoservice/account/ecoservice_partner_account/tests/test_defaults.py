# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup import BaseSetup


class TestDefaults(BaseSetup):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.ID = cls.env['ir.default']
        cls.IP = cls.env['ir.property']

        cls.field_payable = cls.env.ref(
            'account.field_res_partner__property_account_payable_id',
        )
        cls.field_receivable = cls.env.ref(
            'account.field_res_partner__property_account_receivable_id',
        )

    def test_default_payable(self):
        account_type = 'payable'
        field = f'property_account_{account_type}_id'
        field_is_default = f'property_account_{account_type}_is_default'
        default_account = self.IP.get(
            name=field,
            model='res.partner',
        )

        partner = self.RP.create({
            'name': 'Some Company',
        })

        self.assertTrue(
            partner[field_is_default],
        )
        self.assertEqual(
            default_account,
            partner[field],
        )

    def test_default_receivable(self):
        account_type = 'receivable'
        field = f'property_account_{account_type}_id'
        field_is_default = f'property_account_{account_type}_is_default'
        default_account = self.IP.get(
            name=field,
            model='res.partner',
        )

        partner = self.RP.create({
            'name': 'Some Company',
        })

        self.assertTrue(
            partner[field_is_default],
        )
        self.assertEqual(
            default_account,
            partner[field],
        )

    def test_default_payable_with_user_standard(self):
        account_type = 'payable'
        field = f'property_account_{account_type}_id'
        field_is_default = f'property_account_{account_type}_is_default'
        new_account = self.AA.create({
            'company_id': self.env.company.id,
            'code': 'default_test_123',
            'name': 'default_test_123',
            'reconcile': True,
            'user_type_id': self.env.ref(
                f'account.data_account_type_{account_type}',
            ).id,
        })
        default_account = self.IP.get(
            name=field,
            model='res.partner',
        )
        self.ID.create({
            'field_id': self.field_payable.id,
            'json_value': new_account.id,
        })

        partner = self.RP.create({
            'name': 'Some Company',
        })

        self.assertTrue(
            new_account != default_account,
        )
        self.assertTrue(
            partner[field_is_default],
        )
        self.assertEqual(
            new_account,
            partner[field],
        )

    def test_default_receivable_with_user_standard(self):
        account_type = 'receivable'
        field = f'property_account_{account_type}_id'
        field_is_default = f'property_account_{account_type}_is_default'
        new_account = self.AA.create({
            'company_id': self.env.company.id,
            'code': 'default_test_123',
            'name': 'default_test_123',
            'reconcile': True,
            'user_type_id': self.env.ref(
                f'account.data_account_type_{account_type}',
            ).id,
        })
        default_account = self.IP.get(
            name=field,
            model='res.partner',
        )
        self.ID.create({
            'field_id': self.field_receivable.id,
            'json_value': new_account.id,
        })

        partner = self.RP.create({
            'name': 'Some Company',
        })

        self.assertTrue(
            new_account != default_account,
        )
        self.assertTrue(
            partner[field_is_default],
        )
        self.assertEqual(
            new_account,
            partner[field],
        )
