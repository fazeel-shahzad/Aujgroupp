from odoo import http
from odoo.http import request
import json


class MyAllocation(http.Controller):
	@http.route('/my-allocation', type='http', auth='user', website=True)
	def my_allocation(self, **kw):
		abc = request.env['hr.leave.type'].sudo().search([])
	
		
		return http.request.render('portal_user.my_allocation', {'abc': abc})


class JsonCreateForm(http.Controller):
	
	@http.route('/allocation_form', type='http', methods=['POST'], auth="user", website="True")
	def create_allocation(self, **kw):
		rec = kw
		val = rec
		# if request.jsonrequest:
		# if kw['company_name']:
		
		request.env['hr.leave.allocation'].sudo().create({
			'name': kw['name'],
			'number_of_days_display': kw['number_of_days_display'],
			'holiday_status_id': kw['holiday_status_id'],
			# 'holiday' : kw['']
			# # 'attachment_ids': kw['attachment_ids'],
			# 'salary': kw['salary'],
			# 'chamber_commerce': kw['chamber_commerce'],
			# 'message': kw['message'],
		})