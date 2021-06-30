# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from inspect import getmembers

from odoo.fields import Boolean

from odoo.addons.ecoservice_financeinterface.tests.base_setup import BaseSetup


class TestInvoiceExport(BaseSetup):

    def setUp(self):
        super().setUp()

        self._reset_validation_config()

    def _reset_validation_config(self):
        options = self.env['ecofi.validation'].sudo().search([
            ('company_id', '=', self.env.company.id)
        ])
        options.write({
            field: False
            for field
            in getmembers(type(options), lambda x: isinstance(x, Boolean))
        })
