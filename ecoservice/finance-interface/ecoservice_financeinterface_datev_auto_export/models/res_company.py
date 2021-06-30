# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

# Odoo
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # region Fields

    auto_datev_export_config_ids = fields.Many2many(
        comodel_name='auto.datev.export.config',
        string='Auto Mail Export Configuration',
    )

    # endregion
