from odoo import http
from odoo.http import request
import json


class LoanView(http.Controller):
	@http.route('/loan-request-view', type='http', auth="user", website=True)
	def loan_view(self, **kw):
		loan = request.env['hr.loan'].sudo().search([])
		# view = request.env['hr.employee'].search([])

		# abc = loan.state
		# waiting_approval_1
		# if abc:
		# 	abc = "Submitted"
		# i = abc

		return request.render('portal_user.loan_request_view', {
			'loan': loan,
			# 'abc':abc,
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
