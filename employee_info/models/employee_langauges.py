# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeLanguages(models.Model):
    _name = 'employee.languages'
    _description = "Employee Languages"

    emp_lang_line = fields.Many2one('hr.employee', string="Employee Languages")
    language = fields.Char("Language")
    level = fields.Selection([('average', 'Average'),('good','Good'), ('excellent','Excellent')])