# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTemplateIn(models.Model):
    _inherit = 'product.template'

    def _default_branch_id(self):
        branch_id = self.env['res.users'].browse(self._uid).branch_id.id
        return [branch_id]

    branch_ids = fields.Many2many('res.branch', 'res_branch_product_id', 'branch_id', 'product_id', default=_default_branch_id)
