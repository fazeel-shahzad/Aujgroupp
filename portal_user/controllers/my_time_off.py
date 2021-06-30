from odoo import http
from odoo.http import request
import json


class MyTime(http.Controller):
	@http.route('/my-time-off-request', type='http', auth='user', website=True)
	def my_time_off(self, **kw):
		res = kw
		# hr = request.env[].search([])
		
		# hr_leave = request.env['hr.leave'].create({
		# 	# 'holiday_status_id' :
		# })
		#
		# leave_type = request.env['hr.leave.type'].create({
		#
		# })
		
		# time_off = request.env['hr.leave.type'].create({
		# 	# # 'name':khan,
		# 	# 'name':kw['holiday_status'],
		# })
		
		# odoo_order = request.env['hr.leave'].create({
		# 	# "holiday_status_id": time_off.id,
		# 	# # 'holiday_status_id': kw['holiday_status_id.name'],
		# 	# 'request_date_from': kw['request_date_from'],
		# 	# 'request_date_to': kw['request_date_to'],
		# 	# 'number_of_days': kw['number_of_days'],
		# 	# 'name': kw['name'],
		# })
		
		return http.request.render('portal_user.my_time_off_request', {
			# 'time_off': time_off
		})


class JsonMyTime(http.Controller):
	@http.route('/create-my-time-request', type='http', methods=['POST'], auth="user", website="True")
	def create_my_time(self, **kw):
		rec = kw
		val = rec
# if request.jsonrequest:
# if kw['company_name']:
# i = kw['holiday_status_id']
# request.env['hr.leave.type'].sudo().create({
# 	'name': kw['name'],
# })

# request.env['hr.leave'].sudo().create({
# 	# 'holiday_status_id': kw['holiday_status_id.name'],
# 	'request_date_from': kw['request_date_from'],
# 	'request_date_to': kw['request_date_to'],
# 	'number_of_days': kw['number_of_days'],
# 	'name': kw['name'],
# 	# 'chamber_commerce': kw['chamber_commerce'],
# 	# 'message': kw['message'],
# })
