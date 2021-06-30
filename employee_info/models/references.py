# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeReferences(models.Model):
    _name = 'employee.references'
    _description = "Employee References"

    employee_reference = fields.Many2one("hr.employee", string="Employee Reference")
    name = fields.Char("Name")
    email = fields.Char("Email")
    contact_no = fields.Char("Contact No")
    occupation = fields.Char("Occupation")