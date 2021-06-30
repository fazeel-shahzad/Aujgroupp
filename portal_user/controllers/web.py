# -*- coding: utf-8 -*-
from odoo import http


class WebController(http.Controller):
	@http.route('/web-page', type='http', auth='public', website=True)
	def web_page(self, **kw):
		return http.request.render('portal_user.web_page')