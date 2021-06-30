from odoo import http
from odoo.http import request
from odoo.tools import format_date


class Attendance(http.Controller):
	@http.route('/attendance', type='http', auth='public', website=True)
	def attendance(self, **kw):
		hr_employee = request.env['hr.employee'].sudo().search([])
		attand = request.env['hr.attendance'].sudo().search([])
		for attend in attand:
			if attend.check_in and attend.check_out:
				delta = attend.check_out - attend.check_in
				attend.worked_hours = delta.total_seconds() / 3600.0
		# abc = ("in", attend.check_in, attend.check_out)
		
		return http.request.render('portal_user.attendance', {'hr_employee': hr_employee, 'attand': attand})


class JsonAttendanceForm(http.Controller):
	@http.route('/attendance-form', type='http', methods=['POST'], auth="user", website="True")
	def create_attendance(self, **kw):
		rec = kw
		val = rec
		# if request.jsonrequest:
		# if kw['company_name']:
		request.env['hr.attendance'].sudo().create({
			'employee_id': kw['employee_id'],
			'check_in': kw['check_in'],
			'check_out': kw['check_out'],
			'worked_hours': kw['worked_hours'],
			# 'reason': kw['reason'],
			# 'state': 'submit',
		})
# return request.redirect('/my')