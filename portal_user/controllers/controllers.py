# -*- coding: utf-8 -*-
# from odoo import http
#
#
# class PortalUser(http.Controller):
# 	@http.route('/dashboard', type='http', auth='public', website=True)
# 	def dashboard(self, **kw):
# 		return http.request.render('portal_user.dashboard')

#     @http.route('/portal_user/portal_user/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('portal_user.listing', {
#             'root': '/portal_user/portal_user',
#             'objects': http.request.env['portal_user.portal_user'].search([]),
#         })

#     @http.route('/portal_user/portal_user/objects/<model("portal_user.portal_user"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('portal_user.object', {
#             'object': obj
#         })
