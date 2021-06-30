from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    commission_structure_id = fields.Many2one('commission.structure.ecotech', 'Commission Structure')