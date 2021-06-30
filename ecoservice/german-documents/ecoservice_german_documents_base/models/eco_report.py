# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class EcoReportMixIn(models.AbstractModel):
    _name = 'eco_report.mixin'

    _description = 'Eco Report Mixin'

    # region Fields
    report_compute_date = fields.Date(
        compute='_compute_date',
    )
    report_line_index = fields.Integer(
        default=1,
    )
    # endregion

    # region Compute Methods
    def _compute_date(self):
        for rec in self:
            # Prevent CacheMiss Exception (#13000)
            rec.report_compute_date = False
    # endregion

    # region Business Methods
    def set_report_line_index(self, value):
        self.report_line_index = value

    def eco_report_prefix(self):
        return '_'.join(self._get_prefixes())

    def eco_report_suffix(self):
        return '_'.join(
            [
                x for x
                in self.mapped(self._get_name_field())
                if x and x != '/'
            ]
        )

    def eco_report_name(self):
        return '-'.join(
            x for x
            in [
                self.eco_report_prefix(),
                self.eco_report_suffix(),
            ]
            if x
        )

    @staticmethod
    def is_html_field_empty(**kwargs):
        blank = ['<p><br></p>', '<p>&nbsp;</p>']

        if kwargs['vals'].get(kwargs['field_name1']) in blank:
            kwargs['vals'][kwargs['field_name1']] = False

        if kwargs['vals'].get(kwargs['field_name2']) in blank:
            kwargs['vals'][kwargs['field_name2']] = False

        return kwargs['vals']

    @api.model
    def _get_name_field(self):
        return 'name'

    def _get_prefixes(self):
        return []
    # endregion
