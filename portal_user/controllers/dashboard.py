from odoo import http
from odoo.http import request
import json



class UserDashboard(http.Controller):
	@http.route('/dashboard', type='http', auth='user', website=True)
	def dashboard(self, **kw):
		# later data
		
		attends = request.env['hr.attendance'].sudo().search([])
		attend_id = attends.ids
		attend_count = len(attend_id)
		#
		# <--request-loan-data---->
		loan_data = request.env['hr.loan'].sudo().search([])
		loan_id = loan_data.ids
		loan_count = len(loan_id)
		
		advance_salary_data = request.env['salary.advance'].sudo().search([])
		salary_id = advance_salary_data.ids
		salary_count = len(salary_id)
		my_data = {
			'loan_count': [loan_count],
			'val_dict': [attend_count],
			'salary_count': [salary_count]
		}
		
		
		# val.update(loan_dict)
		
		return http.request.render('portal_user.dashboard', my_data)