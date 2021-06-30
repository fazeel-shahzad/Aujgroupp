# -*- coding: utf-8 -*-
# from odoo import http


# class InheritDeliveryNew(http.Controller):
#     @http.route('/inherit_delivery_new/inherit_delivery_new/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inherit_delivery_new/inherit_delivery_new/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inherit_delivery_new.listing', {
#             'root': '/inherit_delivery_new/inherit_delivery_new',
#             'objects': http.request.env['inherit_delivery_new.inherit_delivery_new'].search([]),
#         })

#     @http.route('/inherit_delivery_new/inherit_delivery_new/objects/<model("inherit_delivery_new.inherit_delivery_new"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inherit_delivery_new.object', {
#             'object': obj
#         })
