# -*- coding: utf-8 -*-
# from odoo import http


# class GodownShifiting(http.Controller):
#     @http.route('/godown_shifiting/godown_shifiting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/godown_shifiting/godown_shifiting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('godown_shifiting.listing', {
#             'root': '/godown_shifiting/godown_shifiting',
#             'objects': http.request.env['godown_shifiting.godown_shifiting'].search([]),
#         })

#     @http.route('/godown_shifiting/godown_shifiting/objects/<model("godown_shifiting.godown_shifiting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('godown_shifiting.object', {
#             'object': obj
#         })
