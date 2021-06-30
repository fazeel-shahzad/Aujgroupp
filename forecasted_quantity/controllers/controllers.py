# -*- coding: utf-8 -*-
# from odoo import http


# class ForecastedQuantity(http.Controller):
#     @http.route('/forecasted_quantity/forecasted_quantity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/forecasted_quantity/forecasted_quantity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('forecasted_quantity.listing', {
#             'root': '/forecasted_quantity/forecasted_quantity',
#             'objects': http.request.env['forecasted_quantity.forecasted_quantity'].search([]),
#         })

#     @http.route('/forecasted_quantity/forecasted_quantity/objects/<model("forecasted_quantity.forecasted_quantity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('forecasted_quantity.object', {
#             'object': obj
#         })
