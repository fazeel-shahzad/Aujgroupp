# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritDelivery(models.Model):
    _inherit = 'stock.move.line'

    article_no = fields.Char("Article")
    finish = fields.Char("Finish")


class InheritPicking(models.Model):
    _inherit = 'stock.picking'

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
