# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class tax_on_line(models.Model):
#     _name = 'tax_on_line.tax_on_line'
#     _description = 'tax_on_line.tax_on_line'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
