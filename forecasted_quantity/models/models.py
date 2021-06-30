# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ForecastedInherit(models.Model):
    _inherit = 'purchase.order.line'

    forecast_qty=fields.Float("Forecasted Quantity",compute="forcasted_total_qty")
    forecast=fields.Many2one("product.product")
    @api.onchange('product_id')
    def onchange_forecast(self):
        for i in self:
            i.forecast_qty= i.product_id.virtual_available
    @api.depends('product_qty')
    def forcasted_total_qty(self):
        for i in self:
            i.forecast_qty = i.product_id.virtual_available


class ForecastedInherit(models.Model):
    _inherit = 'product.template'






