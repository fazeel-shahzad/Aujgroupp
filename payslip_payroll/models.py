# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class payroll(models.Model):
    _inherit = 'hr.payslip'

    month = fields.Char("Month", compute="compute_month")
    year = fields.Char("Year", compute="compute_year")
    dept = fields.Char("Department")
    # date = fields.Date("Date")
    date_start = fields.Char("Date To", compute="compute_dates")
    amount_in_word = fields.Char("Amount In Words", compute="amount_in_words")

    def amount_in_words(self):
        currency_id = self.env['res.currency'].search([('name', '=', 'PKR')], limit=1)
        print('as', currency_id)
        word = ''
        for i in self.line_ids:
            if i.name == 'Net Salary':
                word = str(currency_id.amount_to_text(i.amount)) + 's only.'
        self.amount_in_word = word

    def compute_month(self):
        for i in self:
            a = i.date_from.strftime("%B")
            i.month = a

    def compute_year(self):
        for i in self:
            a = i.date_from.strftime("%Y")
            i.year = a

    def compute_dates(self):
        for i in self:
            datetimeobject = datetime.strptime(str(i.date_from), '%Y-%m-%d')
            print('az', datetimeobject)
            newformat = datetimeobject.strftime('%d-%B-%Y')
            i.date_start = newformat
            print("a", newformat)

    def allowance_deduction_compute(self):
        for i in self.line_ids:
            obj = self.env['hr.contract'].search([('employee_id.id', '=', self.employee_id.id)])
            for j in obj:
                if i.name == 'Conveyance':
                    i.amount = j.conveyance
                if i.name == 'Mobile Allowance':
                    i.amount = j.mobile_allowance
                if i.name == 'Meal Allowance':
                    i.amount = j.meal_allowance
                if i.name == 'Other':
                    i.amount = j.other
                if i.name == 'Income Tax':
                    i.amount = j.income_tax
                if i.name == 'Advances':
                    i.amount = j.advances
                if i.name == 'EOBI':
                    i.amount = j.eobi
                if i.name == 'Provident Fund':
                    i.amount = j.provident_fund
                if i.name == 'PESSI':
                    i.amount = j.pessi
                if i.name == 'Other Deductions':
                    i.amount = j.other_deductions

        for rec in self.line_ids:
            if rec.amount == 0:
                rec.unlink()


class AddAllowancesDeduction(models.Model):
    _inherit = 'hr.contract'

    conveyance = fields.Float("Conveyance")
    mobile_allowance = fields.Float("Mobile Allowance")
    meal_allowance = fields.Float("Meal Allowance")
    other = fields.Float("Other")
    income_tax = fields.Float("Income Tax")
    advances = fields.Float("Advances")
    eobi = fields.Float("EOBI")
    provident_fund = fields.Float("Provident Fund")
    pessi = fields.Float("PESSI")
    other_deductions = fields.Float("Other Deductions")


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    payment_mode = fields.Selection([('cash', 'Cash'), ('bank_transfer', 'Bank Transfer')], string="Payment Mode")

