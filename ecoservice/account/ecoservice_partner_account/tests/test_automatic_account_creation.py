# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields

from .base_setup import BaseSetup


class TestAutomaticAccountCreation(BaseSetup):

    def setUp(self):
        super(TestAutomaticAccountCreation, self).setUp()

        self.company_1.partner_account_generate_automatically = True

    def test_00_create_no_account_if_automatic_creation_is_not_set(self):
        self.company_1.partner_account_generate_automatically = False

        # Default context from customer menu action
        context = {
            'search_default_customer': 1,
            'res_partner_search_mode': 'customer',
            'default_is_company': True,
            'default_customer_rank': 1,
        }
        partner = self.RP.with_context(**context).create({
            'name': 'Bruce Wayne Enterprises',
        })

        self.assertTrue(
            partner.property_account_receivable_is_default,
        )
        self.assertTrue(
            partner.property_account_payable_is_default,
        )

    def test_create_customer_account_via_customer_menu(self):
        # Default context from customer menu action
        context = {
            'search_default_customer': 1,
            'res_partner_search_mode': 'customer',
            'default_is_company': True,
            'default_customer_rank': 1,
        }
        partner = self.RP.with_context(**context).create({
            'name': 'Bruce Wayne Enterprises',
        })

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

    def test_create_customer_account_via_out_invoice(self):
        partner = self.partner
        partner.is_company = True
        invoice = self.AM.create({
            'partner_id': partner.id,
            'type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Plunder',
                }),
            ]
        })

        invoice.action_post()

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

    def test_create_supplier_account_via_supplier_menu(self):
        # Default context from supplier menu action
        context = {
            'search_default_supplier': 1,
            'res_partner_search_mode': 'supplier',
            'default_is_company': True,
            'default_supplier_rank': 1,
        }
        partner = self.RP.with_context(**context).create({
            'name': 'Bruce Wayne Enterprises',
        })

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

    def test_create_supplier_account_via_in_invoice(self):
        partner = self.partner
        partner.is_company = True
        invoice = self.AM.create({
            'partner_id': partner.id,
            'type': 'in_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Plunder',
                }),
            ]
        })

        invoice.action_post()

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

    def test_create_no_account_via_contact_menu(self):
        # Default context from contact menu action
        context = {
            'default_is_company': True,
        }
        partner = self.RP.with_context(**context).create({
            'name': 'Bruce Wayne Enterprises',
        })

        self.assertTrue(
            partner.property_account_receivable_is_default,
        )
        self.assertTrue(
            partner.property_account_payable_is_default,
        )

    def test_updated_account_in_out_invoice(self):
        partner = self.partner
        partner.is_company = True
        invoice = self.AM.create({
            'partner_id': partner.id,
            'type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Plunder',
                }),
            ]
        })

        invoice.action_post()

        self.assertEqual(
            partner.property_account_receivable_id,
            invoice.line_ids.filtered(
                lambda l: l.account_internal_type == 'receivable',
            ).account_id,
        )

    def test_updated_account_in_in_invoice(self):
        partner = self.partner
        partner.is_company = True
        invoice = self.AM.create({
            'partner_id': partner.id,
            'type': 'in_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Plunder',
                }),
            ]
        })

        invoice.action_post()

        self.assertEqual(
            partner.property_account_payable_id,
            invoice.line_ids.filtered(
                lambda l: l.account_internal_type == 'payable',
            ).account_id,
        )

    def test_no_account_creation_if_standard_move(self):
        partner = self.partner
        journal = self.AJ.search(
            [
                ('company_id', '=', self.company_1.id),
                ('type', '=', 'bank'),  # bank journals have default accounts
            ],
            limit=1,
        )
        move = self.AM.create({
            'partner_id': partner.id,
            'type': 'entry',
            'journal_id': journal.id,
            'date': fields.Date.today(),
            'line_ids': [
                (0, 0, {
                    'account_id': partner.property_account_receivable_id.id,
                    'partner_id': partner.id,
                    'debit': 50.00,
                }),
                (0, 0, {
                    'account_id': journal.default_debit_account_id.id,
                    'partner_id': partner.id,
                    'credit': 50.00,
                }),
            ]
        })

        move.post()

        self.assertTrue(
            partner.property_account_receivable_is_default,
        )
        self.assertTrue(
            partner.property_account_payable_is_default,
        )

    def test_create_account_in_commercial_partner(self):
        # Bug #12920
        self.company_1.partner_account_generate_automatically = False

        account_type = 'property_account_receivable_id'
        company = self.RP.create({
            'name': 'Wayne Enterprise',
            'is_company': True,
        })

        partner = self.partner
        partner.parent_id = company
        account = self.RP.default_get([account_type])[account_type]
        invoice = self.AM.create({
            'partner_id': partner.id,
            'type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': 'Plunder',
                }),
            ]
        })

        self.company_1.partner_account_generate_automatically = True

        invoice.action_post()

        self.assertFalse(
            company.property_account_receivable_is_default,
        )
        self.assertFalse(
            partner.property_account_receivable_is_default,
        )

        self.assertNotEqual(
            account,
            company.property_account_receivable_id.id,
        )
        self.assertNotEqual(
            account,
            partner.property_account_receivable_id.id,
        )

        self.assertEqual(
            company.property_account_receivable_id,
            partner.property_account_receivable_id,
        )
