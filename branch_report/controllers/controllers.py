# -*- coding: utf-8 -*-
# from odoo import http


# class BranchReport(http.Controller):
#     @http.route('/branch_report/branch_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/branch_report/branch_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('branch_report.listing', {
#             'root': '/branch_report/branch_report',
#             'objects': http.request.env['branch_report.branch_report'].search([]),
#         })

#     @http.route('/branch_report/branch_report/objects/<model("branch_report.branch_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('branch_report.object', {
#             'object': obj
#         })
