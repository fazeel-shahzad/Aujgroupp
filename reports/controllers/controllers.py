# -*- coding: utf-8 -*-
# from odoo import http


# class Text(http.Controller):
#     @http.route('/text/text/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/text/text/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('text.listing', {
#             'root': '/text/text',
#             'objects': http.request.env['text.text'].search([]),
#         })

#     @http.route('/text/text/objects/<model("text.text"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('text.object', {
#             'object': obj
#         })
