# -*- coding: utf-8 -*-
from odoo import http

# class CustomAddons/darazConnector/(http.Controller):
#     @http.route('/custom_addons/daraz_connector//custom_addons/daraz_connector//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_addons/daraz_connector//custom_addons/daraz_connector//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_addons/daraz_connector/.listing', {
#             'root': '/custom_addons/daraz_connector//custom_addons/daraz_connector/',
#             'objects': http.request.env['custom_addons/daraz_connector/.custom_addons/daraz_connector/'].search([]),
#         })

#     @http.route('/custom_addons/daraz_connector//custom_addons/daraz_connector//objects/<model("custom_addons/daraz_connector/.custom_addons/daraz_connector/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_addons/daraz_connector/.object', {
#             'object': obj
#         })