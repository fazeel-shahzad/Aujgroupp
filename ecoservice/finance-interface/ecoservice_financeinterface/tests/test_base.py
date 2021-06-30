# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from .base_setup import BaseSetup


class TestBase(BaseSetup):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.AM = cls.env['account.move']
        cls.PP = cls.env['product.product']
        cls.RP = cls.env['res.partner'].with_context(
            no_reset_password=True,
            mail_create_nosubscribe=True,
            mail_create_nolog=True,
        )

        cls.customer = cls.RP.create({
            'name': 'Kunde GmbH',
            'email': 'customer@localhost',
            'customer_rank': 1,
            'supplier_rank': 1,
        })

    def test_00_create_standard_invoice(self):
        try:
            self._create_invoice()
        except Exception as e:
            self.fail('Unexpected exception was raised: {}'.format(e))

    def test_01_post_standard_invoice(self):
        invoice = self._create_invoice()
        try:
            invoice.action_post()
        except Exception as e:
            self.fail('Unexpected exception was raised: {}'.format(e))
