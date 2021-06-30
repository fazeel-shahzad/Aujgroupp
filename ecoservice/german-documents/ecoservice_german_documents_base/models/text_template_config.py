# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class TextTemplateConfig(models.Model):
    _name = 'text.template.config'
    _description = 'Text Template Config'

    # region Fields
    name = fields.Char(
        string='Description',
        help='Text field, which will be printed in the documents.',
        readonly=True,
        translate=True,
    )
    model = fields.Many2one(
        comodel_name='ir.model',
        readonly=True,
    )
    default_text = fields.Text(
        translate=True,
    )
    # endregion

    # region Business Methods
    def get_template_text(self, lang, field_xml_list):
        lang = lang or self.env.user.lang or 'en_US'
        return {
            field: self.env.ref(xml_id).with_context(lang=lang).default_text
            for field, xml_id
            in field_xml_list
        }
    # endregion
