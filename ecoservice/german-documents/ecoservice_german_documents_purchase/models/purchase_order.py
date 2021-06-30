# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import _, api, fields, models


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order', 'eco_report.mixin']

    # region Fields
    purchase_rfq = fields.Html(
        string='Request for Quotation (Top)',
    )
    purchase_confirmation = fields.Html(
        string='Purchase Order (Top)',
    )
    purchase_rfq_bottom = fields.Html(
        string='Request for Quotation (Bottom)',
    )
    purchase_confirmation_bottom = fields.Html(
        string='Purchase Order (Bottom)',
    )
    # endregion

    # region Compute Methods
    def _compute_date(self):
        for rec in self:
            rec.report_compute_date = fields.Date.context_today(
                rec,
                fields.Datetime.from_string(rec.date_order or '')
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
                not self.purchase_rfq
                or self.purchase_rfq == '<p><br></p>'
            ):
                field_xml_list.append((
                    'purchase_rfq',
                    'ecoservice_german_documents_purchase.purchase_rfq_text',
                ))

            if (
                not self.purchase_rfq_bottom
                or self.purchase_rfq_bottom == '<p><br></p>'
            ):
                field_xml_list.append((
                    'purchase_rfq_bottom',
                    'ecoservice_german_documents_purchase.purchase_rfq_text_bottom',
                ))

            if (
                not self.purchase_confirmation
                or self.purchase_confirmation == '<p><br></p>'
            ):
                field_xml_list.append((
                    'purchase_confirmation',
                    'ecoservice_german_documents_purchase.purchase_order_text',
                ))

            if (
                not self.purchase_confirmation_bottom
                or self.purchase_confirmation_bottom == '<p><br></p>'
            ):
                field_xml_list.append((
                    'purchase_confirmation_bottom',
                    'ecoservice_german_documents_purchase.purchase_order_text_bottom',
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
            field_name1='purchase_rfq',
            field_name2='purchase_confirmation',
        )
        rfq = super(PurchaseOrder, self).create(values)
        rfq.get_template_text()
        return rfq

    def write(self, values):
        values = self.is_html_field_empty(
            vals=values,
            field_name1='purchase_rfq',
            field_name2='purchase_confirmation',
        )
        return super(PurchaseOrder, self).write(values)
    # endregion

    # region Business Methods
    def _get_prefixes(self):
        quot = any(r.state in ['draft', 'sent', 'to approve'] for r in self)
        oc = any(r.state in ['purchase', 'done'] for r in self)
        return [x for x in [quot and _('RfQ'), oc and _('PO')] if x]
    # endregion
