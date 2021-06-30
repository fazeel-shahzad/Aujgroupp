# -*- coding: utf-8 -*-
# from odoo import http


# class SaleLineProductImage(http.Controller):
#     @http.route('/sale_line_product_image/sale_line_product_image/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_line_product_image/sale_line_product_image/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_line_product_image.listing', {
#             'root': '/sale_line_product_image/sale_line_product_image',
#             'objects': http.request.env['sale_line_product_image.sale_line_product_image'].search([]),
#         })

#     @http.route('/sale_line_product_image/sale_line_product_image/objects/<model("sale_line_product_image.sale_line_product_image"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_line_product_image.object', {
#             'object': obj
#         })
