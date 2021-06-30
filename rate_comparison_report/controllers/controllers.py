# -*- coding: utf-8 -*-
# from odoo import http


# class RateComparisonReport(http.Controller):
#     @http.route('/rate_comparison_report/rate_comparison_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rate_comparison_report/rate_comparison_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rate_comparison_report.listing', {
#             'root': '/rate_comparison_report/rate_comparison_report',
#             'objects': http.request.env['rate_comparison_report.rate_comparison_report'].search([]),
#         })

#     @http.route('/rate_comparison_report/rate_comparison_report/objects/<model("rate_comparison_report.rate_comparison_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rate_comparison_report.object', {
#             'object': obj
#         })
