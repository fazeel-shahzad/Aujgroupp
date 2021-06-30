# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class pos_session(models.Model):
    _inherit = 'pos.session'

    '''@api.model
    def _get_pos_session_default_branch(self):
        user_pool = self.env['res.users']
        branch_id = user_pool.browse(self.env.uid).branch_id.id  or False
        return branch_id'''

    @api.model
    def create(self,vals):
        res = super(pos_session, self).create(vals)
        user_pool = self.env['res.users']
        res.branch_id = user_pool.browse(self.env.uid).branch_id.id  or False
        return res

    branch_id = fields.Many2one('res.branch', 'Branch')  
