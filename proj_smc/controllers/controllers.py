# -*- coding: utf-8 -*-
# from odoo import http


# class ProjSmc(http.Controller):
#     @http.route('/proj_smc/proj_smc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proj_smc/proj_smc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proj_smc.listing', {
#             'root': '/proj_smc/proj_smc',
#             'objects': http.request.env['proj_smc.proj_smc'].search([]),
#         })

#     @http.route('/proj_smc/proj_smc/objects/<model("proj_smc.proj_smc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proj_smc.object', {
#             'object': obj
#         })
