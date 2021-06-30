# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'eco_report.mixin']

    # region Fields
    account_invoice = fields.Html(
        string='Invoice (Top)',
    )
    account_refund = fields.Html(
        string='Refund (Top)',
    )
    account_invoice_bottom = fields.Html(
        string='Invoice (Bottom)',
    )
    account_refund_bottom = fields.Html(
        string='Refund (Bottom)',
    )

    # endregion

    # region Compute Methods
    def _compute_date(self):
        for rec in self:
            rec.report_compute_date = fields.Date.context_today(
                rec,
                fields.Datetime.from_string(rec.invoice_date or ''),
            )

    # endregion

    # region Onchange Methods
    @api.onchange('partner_id')
    def get_template_text(self):
        # While changing partner: change the text according to partner's language
        # and do not reset this if text is written manually

        if self.partner_id:
            field_xml_list = []
            if (
                not self.account_invoice
                or self.account_invoice == '<p><br></p>'
            ):
                field_xml_list.append((
                    'account_invoice',
                    'ecoservice_german_documents_invoice.account_invoice_text',
                ))

            if (
                not self.account_invoice_bottom
                or self.account_invoice_bottom == '<p><br></p>'
            ):
                field_xml_list.append((
                    'account_invoice_bottom',
                    'ecoservice_german_documents_invoice.account_invoice_text_bottom',
                ))

            if (
                not self.account_refund
                or self.account_refund == '<p><br></p>'
            ):
                field_xml_list.append((
                    'account_refund',
                    'ecoservice_german_documents_invoice.account_refund_text',
                ))

            if (
                not self.account_refund_bottom
                or self.account_refund_bottom == '<p><br></p>'
            ):
                field_xml_list.append((
                    'account_refund_bottom',
                    'ecoservice_german_documents_invoice.account_refund_text_bottom',
                ))

            vals = self.env['text.template.config'].get_template_text(
                self.partner_id.lang,
                field_xml_list,
            )
            self.update(vals)

    # endregion

    # region CRUD Methods
    @api.model
    def create(self, values):
        values = self.is_html_field_empty(
            vals=values,
            field_name1='account_invoice',
            field_name2='account_refund',
        )
        invoice = super(AccountMove, self).create(values)
        invoice.get_template_text()
        return invoice

    def write(self, values):
        values = self.is_html_field_empty(
            vals=values,
            field_name1='account_invoice',
            field_name2='account_refund',
        )
        return super(AccountMove, self).write(values)

    # endregion

    # region Business Methods
    def _get_prefixes(self):
        # Throw exception if there are records that should not be printed
        self._get_report_base_filename()

        invoice = any('invoice' in r.type for r in self)
        refund = any('refund' in r.type for r in self)

        return [
            x for x
            in [
                invoice and _('Invoice'),
                refund and _('Refund'),
            ]
            if x
        ]
    # endregion
