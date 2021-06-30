# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.
from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):
    """Tests for the account change and internal reference write."""

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.AccountInvoice = self.env['account.move']
        self.ResPartner = self.env['res.partner']
        self.PaymentTerm = self.env.ref(
            'account.account_payment_term_immediate'
        )

        # Case 1: Invoice Send Type is not determined
        self.partner_without_invoice_send = self.ResPartner.create({
            'name': 'Partner without InvoiceSend',
            'invoice_send_type': False,
            'property_payment_term_id': self.PaymentTerm.id,
        })
        # Case 2: Invoice Send Type is print
        self.partner_with_print = self.ResPartner.create({
            'name': 'Partner with print',
            'invoice_send_type': 'print'
        })
        # Case 3: Invoice Send Type is email
        self.partner_with_email = self.ResPartner.create({
            'name': 'Partner with email',
            'invoice_send_type': 'email'
        })

    def test_create(self):
        """Test create method."""
        # Case 1: Invoice Send Type is not determined
        invoice_0 = self.AccountInvoice.create({
            'partner_id': self.partner_without_invoice_send.id,
        })
        self.assertEqual(
            invoice_0.invoice_send_type,
            self.partner_without_invoice_send.invoice_send_type
        )

        # Case 2: Invoice Send Type is print
        invoice_1 = self.AccountInvoice.create({
            'partner_id': self.partner_with_print.id,
        })
        self.assertEqual(
            invoice_1.invoice_send_type,
            self.partner_with_print.invoice_send_type
        )

        # Case 3: Invoice Send Type is email
        invoice_2 = self.AccountInvoice.create({
            'partner_id': self.partner_with_email.id,
        })
        self.assertEqual(
            invoice_2.invoice_send_type,
            self.partner_with_email.invoice_send_type
        )

    def test_onchange_partner_id(self):
        """Test _onchange_partner_id_invoice_send_type."""
        # Invoice Send Type is not determined
        invoice_0 = self.AccountInvoice.create({
            'partner_id': self.partner_without_invoice_send.id,
            'type': 'out_invoice',
        })
        invoice_0._onchange_partner_id()
        self.assertEqual(
            invoice_0.invoice_send_type,
            self.partner_without_invoice_send.invoice_send_type
        )

        # Test if onchange inheritance chain was broken.
        # Payment terms are set by odoo standard onchange (top parent).
        self.assertEqual(
            self.partner_without_invoice_send.property_payment_term_id.id,
            invoice_0.invoice_payment_term_id.id,
        )

        # Test print send type
        invoice_0.partner_id = self.partner_with_print.id
        invoice_0._onchange_partner_id()
        self.assertEqual(
            invoice_0.invoice_send_type,
            self.partner_with_print.invoice_send_type
        )

        # Test email send type
        invoice_0.partner_id = self.partner_with_email.id
        invoice_0._onchange_partner_id()
        self.assertEqual(
            invoice_0.invoice_send_type,
            self.partner_with_email.invoice_send_type
        )
