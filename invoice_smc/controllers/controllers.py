# -*- coding: utf-8 -*-
# from odoo import http


# class InvoneSmc(http.Controller):
#     @http.route('/invone_smc/invone_smc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invone_smc/invone_smc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('invone_smc.listing', {
#             'root': '/invone_smc/invone_smc',
#             'objects': http.request.env['invone_smc.invone_smc'].search([]),
#         })

#     @http.route('/invone_smc/invone_smc/objects/<model("invone_smc.invone_smc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invone_smc.object', {
#             'object': obj
#         })
