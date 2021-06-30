# -*- coding: utf-8 -*-
# from odoo import http


# class SmcProject(http.Controller):
#     @http.route('/smc_project/smc_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smc_project/smc_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smc_project.listing', {
#             'root': '/smc_project/smc_project',
#             'objects': http.request.env['smc_project.smc_project'].search([]),
#         })

#     @http.route('/smc_project/smc_project/objects/<model("smc_project.smc_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smc_project.object', {
#             'object': obj
#         })
