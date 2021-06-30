# -*- coding: utf-8 -*-

from odoo import models, fields, api,_



class ProductProduct(models.Model):
    _inherit = 'product.template'

    parent_sku = fields.Char(string='Parent SKU')









