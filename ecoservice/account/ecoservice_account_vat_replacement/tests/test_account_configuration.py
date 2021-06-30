# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo.tests import common


class TestAccountConfiguration(common.SavepointCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.AA = cls.env['account.account']
        cls.AAT = cls.env['account.account.type']
        cls.AT = cls.env['account.tax']
        cls.ATG = cls.env['account.tax.group']
        cls.PP = cls.env['product.product']
        cls.PC = cls.env['product.category']
        cls.RC = cls.env['res.company']
        cls.VC = cls.env['vat.configuration']
        cls.VCA = cls.env['vat.configuration.account']

        cls.company_1 = cls.env.company
        cls.company_2 = cls.RC.create({
            'name': 'Company 2',
        })

        cls.account_type_income = cls.AAT.create({
            'name': 'Account Type',
            'type': 'other',
            'internal_group': 'income',
        })
        cls.account_type_expense = cls.AAT.create({
            'name': 'Account Type',
            'type': 'other',
            'internal_group': 'expense',
        })

        cls.tax_group_purchase = cls.ATG.create({
            'name': 'Purchase Tax Group',
        })
        cls.tax_group_sale = cls.ATG.create({
            'name': 'Sales Tax Group',
        })

        # region Company 1
        cls.source_income_account_c1 = cls.AA.create({
            'code': 'SourceIncome123',
            'name': 'SourceIncome123',
            'user_type_id': cls.account_type_income.id,
            'company_id': cls.company_1.id,
        })
        cls.source_expense_account_c1 = cls.AA.create({
            'code': 'SourceExpense123',
            'name': 'SourceExpense123',
            'user_type_id': cls.account_type_expense.id,
            'company_id': cls.company_1.id,
        })
        cls.target_income_account_c1 = cls.AA.create({
            'code': 'TargetIncome123',
            'name': 'TargetIncome123',
            'user_type_id': cls.account_type_income.id,
            'company_id': cls.company_1.id,
        })
        cls.target_expense_account_c1 = cls.AA.create({
            'code': 'TargetExpense123',
            'name': 'TargeteExpense123',
            'user_type_id': cls.account_type_expense.id,
            'company_id': cls.company_1.id,
        })

        cls.source_purchase_tax_c1 = cls.AT.create({
            'name': 'Source Purchase Tax',
            'amount': '19.0',
            'amount_type': 'percent',
            'type_tax_use': 'purchase',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_1.id,
        })
        cls.source_sales_tax_c1 = cls.AT.create({
            'name': 'Source Sales Tax',
            'amount': '19.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_1.id,
        })
        cls.target_purchase_tax_c1 = cls.AT.create({
            'name': 'Target Purchase Tax',
            'amount': '16.0',
            'amount_type': 'percent',
            'type_tax_use': 'purchase',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_1.id,
        })
        cls.target_sales_tax_c1 = cls.AT.create({
            'name': 'Target Sales Tax',
            'amount': '16.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_1.id,
        })
        cls.unchanged_sales_tax_c1 = cls.AT.create({
            'name': 'Unchanged Sales Tax',
            'amount': '7.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_1.id,
        })
        cls.unchanged_purchase_tax_c1 = cls.AT.create({
            'name': 'Unchanged Purchase Tax',
            'amount': '7.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_1.id,
        })
        # endregion

        # region Company 2
        cls.source_income_account_c2 = cls.AA.create({
            'code': 'SourceIncome123',
            'name': 'SourceIncome123',
            'user_type_id': cls.account_type_income.id,
            'company_id': cls.company_2.id,
        })
        cls.source_expense_account_c2 = cls.AA.create({
            'code': 'SourceExpense123',
            'name': 'SourceExpense123',
            'user_type_id': cls.account_type_expense.id,
            'company_id': cls.company_2.id,
        })
        cls.target_income_account_c2 = cls.AA.create({
            'code': 'TargetIncome123',
            'name': 'TargetIncome123',
            'user_type_id': cls.account_type_income.id,
            'company_id': cls.company_2.id,
        })
        cls.target_expense_account_c2 = cls.AA.create({
            'code': 'TargetExpense123',
            'name': 'TargeteExpense123',
            'user_type_id': cls.account_type_expense.id,
            'company_id': cls.company_2.id,
        })

        cls.source_purchase_tax_c2 = cls.AT.create({
            'name': 'Source Purchase Tax',
            'amount': '19.0',
            'amount_type': 'percent',
            'type_tax_use': 'purchase',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_2.id,
        })
        cls.source_sales_tax_c2 = cls.AT.create({
            'name': 'Source Sales Tax',
            'amount': '19.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_2.id,
        })
        cls.target_purchase_tax_c2 = cls.AT.create({
            'name': 'Target Purchase Tax',
            'amount': '16.0',
            'amount_type': 'percent',
            'type_tax_use': 'purchase',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_2.id,
        })
        cls.target_sales_tax_c2 = cls.AT.create({
            'name': 'Target Sales Tax',
            'amount': '16.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_2.id,
        })
        cls.unchanged_sales_tax_c2 = cls.AT.create({
            'name': 'Unchanged Sales Tax',
            'amount': '7.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_2.id,
        })
        cls.unchanged_purchase_tax_c2 = cls.AT.create({
            'name': 'Unchanged Purchase Tax',
            'amount': '7.0',
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'tax_group_id': cls.tax_group_sale.id,
            'company_id': cls.company_2.id,
        })
        # endregion

    # region Basic Tests
    def test_no_configuration_no_worries(self):
        try:
            self.VC.run()
        except Exception:
            self.fail('This code should run without exceptions')

    def test_configuring_same_source_account_twice_triggers_exception(self):
        with self.assertRaisesRegex(
            Exception,
            'duplicate key value violates unique constraint',
        ):
            self.VC.create({
                'company_id': self.company_1.id,
                'description': 'desc',
                'configuration_account_ids': [
                    (0, 0, {
                        'source_account_id': self.source_income_account_c1.id,
                        'target_account_id': self.target_income_account_c1.id,
                    }),
                    (0, 0, {
                        'source_account_id': self.source_income_account_c1.id,
                        'target_account_id': self.target_expense_account_c1.id
                    }),
                ],
            })

    def test_configuring_same_source_tax_twice_triggers_exception(self):
        with self.assertRaisesRegex(
            Exception,
            'duplicate key value violates unique constraint',
        ):
            self.VC.create({
                'company_id': self.company_1.id,
                'description': 'desc',
                'configuration_tax_ids': [
                    (0, 0, {
                        'source_tax_id': self.source_sales_tax_c1.id,
                        'target_tax_id': self.target_sales_tax_c1.id,
                    }),
                    (0, 0, {
                        'source_tax_id': self.source_sales_tax_c1.id,
                        'target_tax_id': self.target_purchase_tax_c1.id
                    }),
                ],
            })
    # endregion

    # region Product Tests
    def test_replace_account_in_product(self):
        product = self.PP.create({
            'name': 'Product',
            'property_account_income_id': self.source_income_account_c1.id,
            'property_account_expense_id': self.source_expense_account_c1.id,
        })
        configuration = self.VC.create({
            'company_id': self.env.company.id,
            'description': 'desc',
            'configuration_account_ids': [
                (0, 0, {
                    'source_account_id': self.source_income_account_c1.id,
                    'target_account_id': self.target_income_account_c1.id,
                }),
                (0, 0, {
                    'source_account_id': self.source_expense_account_c1.id,
                    'target_account_id': self.target_expense_account_c1.id,
                }),
            ],
        })

        configuration.run()

        self.assertEqual(
            self.target_income_account_c1,
            product.property_account_income_id,
        )
        self.assertEqual(
            self.target_expense_account_c1,
            product.property_account_expense_id,
        )

    def test_replace_account_in_product_multi_company(self):
        product_c1 = self.PP.with_context(force_company=self.company_1.id).create({
            'name': 'Product',
            'property_account_income_id': self.source_income_account_c1.id,
            'property_account_expense_id': self.source_expense_account_c1.id,
        })

        product_c2 = product_c1.with_context(force_company=self.company_2.id)
        product_c2.write({
            'property_account_income_id': self.source_income_account_c2.id,
            'property_account_expense_id': self.source_expense_account_c2.id,
        })

        configuration_1 = self.VC.create({
            'company_id': self.company_1.id,
            'description': 'desc',
            'configuration_account_ids': [
                (0, 0, {
                    'source_account_id': self.source_income_account_c1.id,
                    'target_account_id': self.target_income_account_c1.id,
                }),
                (0, 0, {
                    'source_account_id': self.source_expense_account_c1.id,
                    'target_account_id': self.target_expense_account_c1.id,
                }),
            ],
        })
        configuration_2 = self.VC.create({
            'company_id': self.company_2.id,
            'description': 'desc',
            'configuration_account_ids': [
                (0, 0, {
                    'source_account_id': self.source_income_account_c2.id,
                    'target_account_id': self.target_income_account_c2.id,
                }),
                (0, 0, {
                    'source_account_id': self.source_expense_account_c2.id,
                    'target_account_id': self.target_expense_account_c2.id,
                }),
            ],
        })

        configuration_1.run()

        # Accounts for company 1 should be replaced by now
        self.assertEqual(
            self.target_income_account_c1,
            product_c1.property_account_income_id,
        )
        self.assertEqual(
            self.target_expense_account_c1,
            product_c1.property_account_expense_id,
        )

        # Make sure that accounts for company 2 are untouched
        self.assertEqual(
            self.source_income_account_c2,
            product_c2.property_account_income_id,
        )
        self.assertEqual(
            self.source_expense_account_c2,
            product_c2.property_account_expense_id,
        )

        configuration_2.run()

        # Make sure that the accounts for company 1 didn't change when conf 2 was run
        self.assertEqual(
            self.target_income_account_c1,
            product_c1.property_account_income_id,
        )
        self.assertEqual(
            self.target_expense_account_c1,
            product_c1.property_account_expense_id,
        )

        # Make sure that the accounts for company 2 have been replaced correctly
        self.assertEqual(
            self.target_income_account_c2,
            product_c2.property_account_income_id,
        )
        self.assertEqual(
            self.target_expense_account_c2,
            product_c2.property_account_expense_id,
        )

    def test_replace_tax_in_product(self):
        product = self.PP.create({
            'name': 'Product',
            'taxes_id': [(6, 0, self.source_sales_tax_c1.ids)],
            'supplier_taxes_id': [(6, 0, self.source_purchase_tax_c1.ids)],
        })
        configuration = self.VC.create({
            'company_id': self.env.company.id,
            'description': 'desc',
            'configuration_tax_ids': [
                (0, 0, {
                    'source_tax_id': self.source_sales_tax_c1.id,
                    'target_tax_id': self.target_sales_tax_c1.id,
                }),
                (0, 0, {
                    'source_tax_id': self.source_purchase_tax_c1.id,
                    'target_tax_id': self.target_purchase_tax_c1.id,
                }),
            ],
        })

        configuration.run()

        self.assertTrue(
            self.target_sales_tax_c1 in product.taxes_id,
        )
        self.assertTrue(
            self.target_purchase_tax_c1 in product.supplier_taxes_id,
        )

    def test_replace_tax_in_product_with_not_to_be_replaced_tax(self):
        purchase_taxes = self.source_purchase_tax_c1 | self.unchanged_purchase_tax_c1
        sales_taxes = self.source_sales_tax_c1 | self.unchanged_sales_tax_c1

        product = self.PP.create({
            'name': 'Product',
            'taxes_id': [(6, 0, sales_taxes.ids)],
            'supplier_taxes_id': [(6, 0, purchase_taxes.ids)],
        })
        configuration = self.VC.create({
            'company_id': self.env.company.id,
            'description': 'desc',
            'configuration_tax_ids': [
                (0, 0, {
                    'source_tax_id': self.source_sales_tax_c1.id,
                    'target_tax_id': self.target_sales_tax_c1.id,
                }),
                (0, 0, {
                    'source_tax_id': self.source_purchase_tax_c1.id,
                    'target_tax_id': self.target_purchase_tax_c1.id,
                }),
            ],
        })

        configuration.run()

        self.assertTrue(
            self.target_sales_tax_c1 in product.taxes_id,
        )
        self.assertTrue(
            self.target_purchase_tax_c1 in product.supplier_taxes_id,
        )
        self.assertTrue(
            self.unchanged_sales_tax_c1 in product.taxes_id
        )
        self.assertTrue(
            self.unchanged_purchase_tax_c1 in product.supplier_taxes_id
        )

    def test_replace_tax_in_product_multi_company(self):
        sales_taxes = (
            self.source_sales_tax_c1
            | self.source_sales_tax_c2
            | self.unchanged_sales_tax_c1
            | self.unchanged_sales_tax_c2
        )
        purchase_taxes = (
            self.source_purchase_tax_c1
            | self.source_purchase_tax_c2
            | self.unchanged_purchase_tax_c1
            | self.unchanged_purchase_tax_c2
        )

        product = self.PP.create({
            'name': 'Product',
            'taxes_id': [(6, 0, sales_taxes.ids)],
            'supplier_taxes_id': [(6, 0, purchase_taxes.ids)],
        })
        configuration_1 = self.VC.create({
            'company_id': self.company_1.id,
            'description': 'desc',
            'configuration_tax_ids': [
                (0, 0, {
                    'source_tax_id': self.source_sales_tax_c1.id,
                    'target_tax_id': self.target_sales_tax_c1.id,
                }),
                (0, 0, {
                    'source_tax_id': self.source_purchase_tax_c1.id,
                    'target_tax_id': self.target_purchase_tax_c1.id,
                }),
            ],
        })
        configuration_2 = self.VC.create({
            'company_id': self.company_2.id,
            'description': 'desc',
            'configuration_tax_ids': [
                (0, 0, {
                    'source_tax_id': self.source_sales_tax_c2.id,
                    'target_tax_id': self.target_sales_tax_c2.id,
                }),
                (0, 0, {
                    'source_tax_id': self.source_purchase_tax_c2.id,
                    'target_tax_id': self.target_purchase_tax_c2.id,
                }),
            ],
        })

        configuration_1.run()

        # Make sure that the taxes of company 1 have been replaced
        self.assertTrue(
            self.target_sales_tax_c1 in product.taxes_id,
        )
        self.assertTrue(
            self.target_purchase_tax_c1 in product.supplier_taxes_id,
        )

        # Make sure that the taxes of company 2 have *not* been changed
        self.assertTrue(
            self.source_sales_tax_c2 in product.taxes_id,
        )
        self.assertTrue(
            self.source_purchase_tax_c2 in product.supplier_taxes_id,
        )

        # Make sure that the taxes that should've not been changed are unchanged
        self.assertTrue(
            self.unchanged_sales_tax_c1 in product.taxes_id
        )
        self.assertTrue(
            self.unchanged_purchase_tax_c1 in product.supplier_taxes_id
        )
        self.assertTrue(
            self.unchanged_sales_tax_c2 in product.taxes_id
        )
        self.assertTrue(
            self.unchanged_purchase_tax_c2 in product.supplier_taxes_id
        )

        configuration_2.run()

        # Make sure that the taxes of company 2 are now changed
        self.assertTrue(
            self.target_sales_tax_c2 in product.taxes_id,
        )
        self.assertTrue(
            self.target_purchase_tax_c2 in product.supplier_taxes_id,
        )

        # Make sure that the taxes of company 1 are still the changed ones
        self.assertTrue(
            self.target_sales_tax_c1 in product.taxes_id,
        )
        self.assertTrue(
            self.target_purchase_tax_c1 in product.supplier_taxes_id,
        )

        # Make sure that the taxes that should've not been changed are still unchanged
        self.assertTrue(
            self.unchanged_sales_tax_c1 in product.taxes_id
        )
        self.assertTrue(
            self.unchanged_purchase_tax_c1 in product.supplier_taxes_id
        )
        self.assertTrue(
            self.unchanged_sales_tax_c2 in product.taxes_id
        )
        self.assertTrue(
            self.unchanged_purchase_tax_c2 in product.supplier_taxes_id
        )
    # endregion

    # region Category Tests
    def test_replace_account_in_category(self):
        category = self.PC.create({
            'name': 'Category',
            'property_account_income_categ_id': self.source_income_account_c1.id,
            'property_account_expense_categ_id': self.source_expense_account_c1.id,
        })
        configuration = self.VC.create({
            'company_id': self.env.company.id,
            'description': 'desc',
            'configuration_account_ids': [
                (0, 0, {
                    'source_account_id': self.source_income_account_c1.id,
                    'target_account_id': self.target_income_account_c1.id,
                }),
                (0, 0, {
                    'source_account_id': self.source_expense_account_c1.id,
                    'target_account_id': self.target_expense_account_c1.id,
                }),
            ],
        })

        configuration.run()

        self.assertEqual(
            self.target_income_account_c1,
            category.property_account_income_categ_id,
        )
        self.assertEqual(
            self.target_expense_account_c1,
            category.property_account_expense_categ_id,
        )

    def test_replace_account_in_category_multi_company(self):
        product_c1 = self.PC.with_context(force_company=self.company_1.id).create({
            'name': 'Product',
            'property_account_income_categ_id': self.source_income_account_c1.id,
            'property_account_expense_categ_id': self.source_expense_account_c1.id,
        })

        product_c2 = product_c1.with_context(force_company=self.company_2.id)
        product_c2.write({
            'property_account_income_categ_id': self.source_income_account_c2.id,
            'property_account_expense_categ_id': self.source_expense_account_c2.id,
        })

        configuration_1 = self.VC.create({
            'company_id': self.company_1.id,
            'description': 'desc',
            'configuration_account_ids': [
                (0, 0, {
                    'source_account_id': self.source_income_account_c1.id,
                    'target_account_id': self.target_income_account_c1.id,
                }),
                (0, 0, {
                    'source_account_id': self.source_expense_account_c1.id,
                    'target_account_id': self.target_expense_account_c1.id,
                }),
            ],
        })
        configuration_2 = self.VC.create({
            'company_id': self.company_2.id,
            'description': 'desc',
            'configuration_account_ids': [
                (0, 0, {
                    'source_account_id': self.source_income_account_c2.id,
                    'target_account_id': self.target_income_account_c2.id,
                }),
                (0, 0, {
                    'source_account_id': self.source_expense_account_c2.id,
                    'target_account_id': self.target_expense_account_c2.id,
                }),
            ],
        })

        configuration_1.run()

        # Accounts for company 1 should be replaced by now
        self.assertEqual(
            self.target_income_account_c1,
            product_c1.property_account_income_categ_id,
        )
        self.assertEqual(
            self.target_expense_account_c1,
            product_c1.property_account_expense_categ_id,
        )

        # Make sure that accounts for company 2 are untouched
        self.assertEqual(
            self.source_income_account_c2,
            product_c2.property_account_income_categ_id,
        )
        self.assertEqual(
            self.source_expense_account_c2,
            product_c2.property_account_expense_categ_id,
        )

        configuration_2.run()

        # Make sure that the accounts for company 1 didn't change when conf 2 was run
        self.assertEqual(
            self.target_income_account_c1,
            product_c1.property_account_income_categ_id,
        )
        self.assertEqual(
            self.target_expense_account_c1,
            product_c1.property_account_expense_categ_id,
        )

        # Make sure that the accounts for company 2 have been replaced correctly
        self.assertEqual(
            self.target_income_account_c2,
            product_c2.property_account_income_categ_id,
        )
        self.assertEqual(
            self.target_expense_account_c2,
            product_c2.property_account_expense_categ_id,
        )
    # endregion
