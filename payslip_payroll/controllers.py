# -*- coding: utf-8 -*-
# from odoo import http


# class Payroll(http.Controller):
#     @http.route('/payroll/payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payroll/payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payroll.listing', {
#             'root': '/payroll/payroll',
#             'objects': http.request.env['payroll.payroll'].search([]),
#         })

#     @http.route('/payroll/payroll/objects/<model("payroll.payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payroll.object', {
#             'object': obj
#         })
