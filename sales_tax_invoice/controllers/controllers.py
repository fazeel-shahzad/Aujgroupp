# -*- coding: utf-8 -*-
# from odoo import http


# class SalesTaxInvoice(http.Controller):
#     @http.route('/sales_tax_invoice/sales_tax_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_tax_invoice/sales_tax_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_tax_invoice.listing', {
#             'root': '/sales_tax_invoice/sales_tax_invoice',
#             'objects': http.request.env['sales_tax_invoice.sales_tax_invoice'].search([]),
#         })

#     @http.route('/sales_tax_invoice/sales_tax_invoice/objects/<model("sales_tax_invoice.sales_tax_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_tax_invoice.object', {
#             'object': obj
#         })
