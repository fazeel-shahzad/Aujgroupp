# -*- coding: utf-8 -*-
# from odoo import http


# class CouriermanagerConnector(http.Controller):
#     @http.route('/couriermanager_connector/couriermanager_connector/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/couriermanager_connector/couriermanager_connector/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('couriermanager_connector.listing', {
#             'root': '/couriermanager_connector/couriermanager_connector',
#             'objects': http.request.env['couriermanager_connector.couriermanager_connector'].search([]),
#         })

#     @http.route('/couriermanager_connector/couriermanager_connector/objects/<model("couriermanager_connector.couriermanager_connector"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('couriermanager_connector.object', {
#             'object': obj
#         })
