from odoo import http
from odoo.http import request
import json


class LoanRequest(http.Controller):
	@http.route('/loan-request', type='http', auth='user', website=True)
	def loan_request(self, **kw):
		e = request.env['hr.loan'].sudo().search([])
		c = request.env['hr.department'].sudo().search([])
		job = request.env['hr.job'].sudo().search([])
		d = request.env['hr.employee'].sudo().search([])
		return http.request.render('portal_user.request_for_loan_form', {
			'e': e,
			'c': c,
			'd': d,
			'job': job
		})


class JsonRequestForm(http.Controller):
	@http.route('/create-loan-request', type='http', methods=['POST'], auth="user", website="True")
	def create_loan(self, **kw):
		rec = kw
		val = rec
		# if request.jsonrequest:
		# if kw['company_name']:
		
		request.env['hr.loan'].sudo().create({
			'employee_id': kw['employee_id'],
			'date': kw['date'],
			'installment': kw['installment'],
			'department_id': kw['department_id'],
			'job_position': kw['job_position'],
			'loan_amount': kw['loan_amount'],
			'state': 'waiting_approval_1',
			# 'chamber_commerce': kw['chamber_commerce'],
			# 'message': kw['message'],
		})
		# return request.redirect('/my')