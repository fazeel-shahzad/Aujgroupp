# -*- coding: utf-8 -*-
from odoo import models, fields
from lxml import etree

class ResUsers(models.Model):
    
    _inherit = 'res.groups'
    
    hide_edit_objects = fields.Many2many('ir.model',string="Hide Button Objects")
    is_hide_edit_group = fields.Boolean("Is hide edit group",default=False)