# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.

# Odoo
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # region Fields

    auto_datev_export_config_ids = fields.Many2many(
        related='company_id.auto_datev_export_config_ids',
        string='Auto Mail Export Configuration',
        readonly=False,
    )

    # endregion

    @api.model
    def get_values(self):
        """
        Overwrite to add new system params.
        """
        res = super(ResConfigSettings, self).get_values()

        env_ir_param = self.env['ir.config_parameter'].sudo()

        param = env_ir_param.get_param('auto_datev_export_config_ids', '[]')

        config_ids = safe_eval(param)
        configs = self.env['auto.datev.export.config'].sudo().search([
            ('id', 'in', config_ids),
        ])

        res.update({
            'auto_datev_export_config_ids': [(6, 0, configs.ids)],
        })
        return res

    @api.model
    def set_values(self):
        """
        Overwrite to add new system params.
        """
        res = super(ResConfigSettings, self).set_values()

        param = self.auto_datev_export_config_ids.ids

        env_ir_param = self.env['ir.config_parameter'].sudo()
        env_ir_param.set_param('auto_datev_export_config_ids', param)

        return res
