# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeInfo(http.Controller):
#     @http.route('/employee_info/employee_info/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_info/employee_info/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_info.listing', {
#             'root': '/employee_info/employee_info',
#             'objects': http.request.env['employee_info.employee_info'].search([]),
#         })

#     @http.route('/employee_info/employee_info/objects/<model("employee_info.employee_info"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_info.object', {
#             'object': obj
#         })
