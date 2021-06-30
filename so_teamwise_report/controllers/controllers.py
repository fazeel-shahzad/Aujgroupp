# -*- coding: utf-8 -*-
# from odoo import http


# class SoTeamwiseReport(http.Controller):
#     @http.route('/so_teamwise_report/so_teamwise_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/so_teamwise_report/so_teamwise_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('so_teamwise_report.listing', {
#             'root': '/so_teamwise_report/so_teamwise_report',
#             'objects': http.request.env['so_teamwise_report.so_teamwise_report'].search([]),
#         })

#     @http.route('/so_teamwise_report/so_teamwise_report/objects/<model("so_teamwise_report.so_teamwise_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('so_teamwise_report.object', {
#             'object': obj
#         })
