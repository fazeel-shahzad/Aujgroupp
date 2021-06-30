# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheriSalePicking(models.Model):
    _inherit = 'stock.move'

    motor_number = fields.Char("Motor Number")
    chassis_no = fields.Char("Chassis No")
    model_number = fields.Char("Model Number")
