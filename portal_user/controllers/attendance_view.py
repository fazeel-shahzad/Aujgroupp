from odoo import http
from odoo.http import request
import json


class AttendanceView(http.Controller):
	@http.route('/attendance-view', type='http', auth='user', website=True)
	def Attendance_View(self, **kw):
		attend = request.env['hr.attendance'].sudo().search([])
		# view = request.env['hr.employee'].search([])
		
		return request.render('portal_user.attendance_view', {
			'attend': attend,
			# 'view':view
		})