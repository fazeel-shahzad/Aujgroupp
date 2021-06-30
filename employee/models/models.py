from odoo import models, fields, api,_


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee Information'


    def _compute_total_year(self):
        total = 0
        for year in self:
            for month in year.com_name:
                print(total)
                total=month.no_of_years+total
            year.total_year = total



    total_year = fields.Float(string='Total No Of Years', compute='_compute_total_year')


    office = fields.One2many("office.use","office_use_only")
    employee_details = fields.One2many("employee.details", "education_info")
    job_type = fields.Many2one("job.type", string="Job Type")
    com_name = fields.One2many("work.history","comp_name")


    father_name = fields.Char(string="Father Name")
    blood_group = fields.Char(string="Blood Group")
    religion = fields.Char(string="Religion")
    birth_date=fields.Date(string="Date Of Birth")
    emails=fields.Char(string="Email")
    Joining_date=fields.Date(string="Date Of Joining")
    marital_status=fields.Selection([('single', 'Single'), ('married', 'Married'), ('widowed', 'Widowed')], string="Marital Status")

class Employee(models.Model):
    _name = 'work.history'
    _description = 'Work History'

    comp_name=fields.Many2one("hr.employee")
    join_date =fields.Date(string="Joining Date")
    end_date =fields.Date(string="Ending Date")
    reason =fields.Char(string="Reason Of Leaving")
    compan_name=fields.Char(string="Company Name")
    no_of_years = fields.Integer("Experience in Years")
    design=fields.Char(string="Designation")
    salari=fields.Char(string="Salary")








class Employee(models.Model):
    _name = 'employee.details'
    _description = 'Employee Details'


    education_info = fields.Many2one("hr.employee", string="Education Info")
    programme = fields.Many2one("program.program", string="Programme")
    degree_title = fields.Char(string="Degree Title")
    grade_div = fields.Char(string="Grade/Div.")
    name_place = fields.Char(string="Name & Place of Institute")
    passing_year = fields.Integer("Passing Year")
    major_sub = fields.Char(string="Major Subjects")
    upload_documents = fields.Binary(string="Upload Certificates & Docs")


class Employee(models.Model):
    _name = 'job.type'
    _description = 'Type Of Job'

    name= fields.Char(string="Job Type")


class Employee(models.Model):
    _name = 'program.program'
    _description = 'Programs'

    name = fields.Char(string="Programme")


class Office(models.Model):
    _name = 'office.use'
    _description = 'For Office Use'

    office_use_only = fields.Many2one("hr.employee",string="Office Use Only")
    joining_date=fields.Date("Joining Date")
    gross_salary=fields.Float("Monthly Salary/Gross Salary")
    incentive=fields.Float("Incentive/Allowance")
















