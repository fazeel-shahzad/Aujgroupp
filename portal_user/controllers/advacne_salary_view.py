from odoo import http
from odoo.http import request
import json


class AdvanceSalary(http.Controller):
	@http.route('/advance-salary-view', type='http', auth='user', website=True)
	def salaryView(self, **kw):
		salary = request.env['salary.advance'].sudo().search([])
		# view = request.env['hr.employee'].search([])
		
		return request.render('portal_user.salary_advance_view', {
			'salary': salary,
			# 'view':view
		})
# val ={
# 	'view' : view
# }
#
# return http.request.render('js_frame_work.latter_request_view',{'view': view})
# latter_display = request.env['employee.letter.request'].search([])
# val = {
# 'emp': emp
# }