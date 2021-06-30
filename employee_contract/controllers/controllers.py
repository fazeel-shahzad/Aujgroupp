# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeContract(http.Controller):
#     @http.route('/employee_contract/employee_contract/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_contract/employee_contract/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_contract.listing', {
#             'root': '/employee_contract/employee_contract',
#             'objects': http.request.env['employee_contract.employee_contract'].search([]),
#         })

#     @http.route('/employee_contract/employee_contract/objects/<model("employee_contract.employee_contract"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_contract.object', {
#             'object': obj
#         })
