# -*- coding: utf-8 -*-
# from odoo import http


# class GoodsReceivedReport(http.Controller):
#     @http.route('/goods_received_report/goods_received_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/goods_received_report/goods_received_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('goods_received_report.listing', {
#             'root': '/goods_received_report/goods_received_report',
#             'objects': http.request.env['goods_received_report.goods_received_report'].search([]),
#         })

#     @http.route('/goods_received_report/goods_received_report/objects/<model("goods_received_report.goods_received_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('goods_received_report.object', {
#             'object': obj
#         })
