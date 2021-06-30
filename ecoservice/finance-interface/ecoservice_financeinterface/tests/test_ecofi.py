# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from .base_setup import BaseSetup


class TestEcoFI(BaseSetup):

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
        })
