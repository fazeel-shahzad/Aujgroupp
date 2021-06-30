# -*- coding: utf-8 -*-
# from odoo import http


# class ReservedQuantity(http.Controller):
#     @http.route('/reserved_quantity/reserved_quantity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reserved_quantity/reserved_quantity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reserved_quantity.listing', {
#             'root': '/reserved_quantity/reserved_quantity',
#             'objects': http.request.env['reserved_quantity.reserved_quantity'].search([]),
#         })

#     @http.route('/reserved_quantity/reserved_quantity/objects/<model("reserved_quantity.reserved_quantity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reserved_quantity.object', {
#             'object': obj
#         })
