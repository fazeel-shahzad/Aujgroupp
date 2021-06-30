# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeePayroll(models.Model):
    _inherit = 'hr.employee'

    program = fields.Selection([
        ('master', 'Master'),
        ('bachelor', 'Bachelor'),
        ('intermediate', 'Intermediate'),
        ('matric_a_level', 'Matric / A-level'),
        ('other', 'Other'),
    ])
    degree_title = fields.Char("Degree Title")
    name_place_institute = fields.Char("Name and Place of institute")
    passing_year = fields.Date("Passing Year")
    grade_div = fields.Char("Grade / Div")
    major_sub = fields.Char("Major Subject")


    #here is the fields for working experience
    work_experience = fields.One2many('employee.work.experience','work_experience_line', string="Employee Work Experience")

    #here is the field for languages
    emp_lang = fields.One2many('employee.languages', 'emp_lang_line', string="Employee Language")

    #here is the fields for disability etc
    disability_state = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Have You Any Disability")
    disability = fields.Text('Disability Explanation')
    allergy_state = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Have You Any Kind Of allergy")
    allergy = fields.Text('Allergy Explanation')
    arrest_state = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Have You Ever Arrested")
    arrest = fields.Text('Arrest Explanation')


    #here is the other fields

    domicile = fields.Char("Domicile")
    permanent_address = fields.Char("Permanent Address")
    join_date = fields.Date("Join Date")
    employee_code = fields.Char("Employee Code")
    per_month_gross_sal = fields.Float("Per Month Gross Salary")
    any_incentives = fields.Integer("Any Incentives")

    employee_reference_line = fields.One2many('employee.references', 'employee_reference', string="Employee Reference")

