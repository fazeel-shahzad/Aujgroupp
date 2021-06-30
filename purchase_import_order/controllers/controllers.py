# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseImportOrder(http.Controller):
#     @http.route('/purchase_import_order/purchase_import_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_import_order/purchase_import_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_import_order.listing', {
#             'root': '/purchase_import_order/purchase_import_order',
#             'objects': http.request.env['purchase_import_order.purchase_import_order'].search([]),
#         })

#     @http.route('/purchase_import_order/purchase_import_order/objects/<model("purchase_import_order.purchase_import_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_import_order.object', {
#             'object': obj
#         })
