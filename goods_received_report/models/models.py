# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class goods_received_report(models.Model):
#     _name = 'goods_received_report.goods_received_report'
#     _description = 'goods_received_report.goods_received_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
