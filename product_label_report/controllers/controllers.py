# -*- coding: utf-8 -*-
# from odoo import http


# class ProductLabelReport(http.Controller):
#     @http.route('/product_label_report/product_label_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_label_report/product_label_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_label_report.listing', {
#             'root': '/product_label_report/product_label_report',
#             'objects': http.request.env['product_label_report.product_label_report'].search([]),
#         })

#     @http.route('/product_label_report/product_label_report/objects/<model("product_label_report.product_label_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_label_report.object', {
#             'object': obj
#         })
