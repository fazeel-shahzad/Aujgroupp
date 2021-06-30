# -*- coding: utf-8 -*-
# from odoo import http


# class DeliveryChallan(http.Controller):
#     @http.route('/delivery_challan/delivery_challan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_challan/delivery_challan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_challan.listing', {
#             'root': '/delivery_challan/delivery_challan',
#             'objects': http.request.env['delivery_challan.delivery_challan'].search([]),
#         })

#     @http.route('/delivery_challan/delivery_challan/objects/<model("delivery_challan.delivery_challan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_challan.object', {
#             'object': obj
#         })
