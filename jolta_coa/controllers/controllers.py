# -*- coding: utf-8 -*-
# from odoo import http


# class JoltaCoa(http.Controller):
#     @http.route('/jolta_coa/jolta_coa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jolta_coa/jolta_coa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jolta_coa.listing', {
#             'root': '/jolta_coa/jolta_coa',
#             'objects': http.request.env['jolta_coa.jolta_coa'].search([]),
#         })

#     @http.route('/jolta_coa/jolta_coa/objects/<model("jolta_coa.jolta_coa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jolta_coa.object', {
#             'object': obj
#         })
