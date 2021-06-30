# -*- coding: utf-8 -*-
# from odoo import http


# class VendorInvoices(http.Controller):
#     @http.route('/vendor_invoices/vendor_invoices/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vendor_invoices/vendor_invoices/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vendor_invoices.listing', {
#             'root': '/vendor_invoices/vendor_invoices',
#             'objects': http.request.env['vendor_invoices.vendor_invoices'].search([]),
#         })

#     @http.route('/vendor_invoices/vendor_invoices/objects/<model("vendor_invoices.vendor_invoices"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vendor_invoices.object', {
#             'object': obj
#         })
