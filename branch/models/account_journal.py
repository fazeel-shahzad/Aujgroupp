from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class Journal(models.Model):
    _inherit = 'account.journal'

    branch_id = fields.Many2one('res.branch', default=lambda r: r.env.user.branch_id.id)
