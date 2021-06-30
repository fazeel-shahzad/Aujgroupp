# -*- coding: utf-8 -*-
# from odoo import http


# class RstInvoice(http.Controller):
#     @http.route('/rst_invoice/rst_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rst_invoice/rst_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rst_invoice.listing', {
#             'root': '/rst_invoice/rst_invoice',
#             'objects': http.request.env['rst_invoice.rst_invoice'].search([]),
#         })

#     @http.route('/rst_invoice/rst_invoice/objects/<model("rst_invoice.rst_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rst_invoice.object', {
#             'object': obj
#         })
