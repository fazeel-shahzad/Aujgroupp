# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import _, api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # region Business Methods
    def get_bank_accounts(self):
        if 'res.partner.bank' not in self.env:
            return []
        return self.env['res.partner.bank'].search(
            [
                ('partner_id', '=', self.id),
            ],
        )

    def get_xml_salutation(self):
        self.ensure_one()

        if (
            self.is_company
            or not (
                self.name
                and self.name.strip()
                and self.title.salutation
            )
        ):
            # Treat as company
            return _('Dear Sir or Madam')

        # Treat as private person
        return '{salutation} {name}'.format(
            salutation=self.title.salutation,
            name=self.lastname if self.has_lastname() else self.name,
        )

    def get_account_journal(self):
        bank_ids = self.env['account.journal'].search(
            [
                ('bank_id', '!=', False),
                ('display_on_footer', '!=', False),
            ],
        )
        return bank_ids

    @api.model
    def has_lastname(self):
        # Check if the field lastname exists in self (res.partner)
        return 'lastname' in self
    # endregion
