from odoo import http
from odoo.http import request
import json


class AdvanceSalary(http.Controller):
	@http.route('/advance-salary', type='http', auth='public', website=True)
	def advance_salary(self, **kw):
		hr_employee = request.env['hr.employee'].sudo().search([])
		hr_department = request.env['hr.department'].sudo().search([])
		
		return http.request.render('portal_user.advance_salary_form', {'hr_employee': hr_employee, 'hr_department': hr_department})


class JsonAdvanceForm(http.Controller):
	@http.route('/advance-salary-form', type='http', methods=['POST'], auth="user", website="True")
	def create_advance(self, **kw):
		rec = kw
		val = rec
		# if request.jsonrequest:
		# if kw['company_name']:
		
		request.env['salary.advance'].sudo().create({
			'employee_id': kw['employee_id'],
			'advance': kw['advance'],
			'department': kw['department'],
			'date': kw['date'],
			'reason': kw['reason'],
			'state': 'submit',
		})
# return request.redirect('/my')
