# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employeecontract(models.Model):
    _inherit = 'hr.contract'

    name = fields.Char( related='employee_id.emp_seq')

