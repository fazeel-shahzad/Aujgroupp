# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResBranch(models.Model):
    _name = 'res.branch'
    _description = 'Branch'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    telephone = fields.Char(string='Telephone No')
    address = fields.Text('Address')
    division_id = fields.Many2one('operating.unit.division', string='Division')

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     branch_ids = []
    #     if self._context.get('branch_id'):
    #         recs = self.search([('id', 'in', self.env.user.branch_ids.ids)] + args, limit=limit, access_rights_uid=name_get_uid)
    #         return recs.name_get()
    #         return models.lazy_name_get(self.browse(branch_ids).with_user(name_get_uid))
    #     return super(ResBranch, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)