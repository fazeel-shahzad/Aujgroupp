# -*- coding: utf-8 -*-
# from odoo import http


# class ReportSmc(http.Controller):
#     @http.route('/report_smc/report_smc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_smc/report_smc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_smc.listing', {
#             'root': '/report_smc/report_smc',
#             'objects': http.request.env['report_smc.report_smc'].search([]),
#         })

#     @http.route('/report_smc/report_smc/objects/<model("report_smc.report_smc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_smc.object', {
#             'object': obj
#         })
