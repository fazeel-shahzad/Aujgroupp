# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeWorkExperice(models.Model):
    _name = 'employee.work.experience'
    _description = "Employee Work Experience"

    work_experience_line = fields.Many2one('hr.employee', string="Work Experience")
    e_job_title = fields.Char("Job Title")
    emp_name_address = fields.Char("Employee Name And Address")
    supervisor_name = fields.Char("Supervisor Name")
    start_from = fields.Date("Start From")
    end_on = fields.Date("End On")
    leave_reason = fields.Text("Reason Of leaving")
    contact = fields.Char("Contact")
    drawn_salary = fields.Char("Drawn Salary")