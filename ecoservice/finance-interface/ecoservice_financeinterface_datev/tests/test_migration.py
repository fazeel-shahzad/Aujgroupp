# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from .base_setup_datev import BaseSetupDatev


class TestMigration(BaseSetupDatev):

    def setUp(self):
        super(BaseSetupDatev, self).setUp()

        self.EMM = self.env['ecofi.move.migration']

    def test_migration_with_deactivated_tax(self):
        invoice = self._create_invoice('out_invoice')

        invoice.invoice_line_ids.tax_ids.active = False

        migration = self.EMM.create({
            'taxes_are_configured': True,
            'accounts_are_configured': True,
        })

        try:
            migration.action_migrate()
        except IndexError:
            self.fail('This should not fail!')
