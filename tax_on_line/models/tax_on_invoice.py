#  -*- coding: utf-8 -*-
 
from odoo import models, fields, api


class Sales_tax_on_line(models.Model):
    _inherit = "sale.order.line"

    tax_amount = fields.Monetary(string='Tax amount', store=True, readonly=True
                                , compute="get_line_tax_amount")

    @api.depends('product_uom_qty', 'tax_id', 'price_unit')
    def get_line_tax_amount(self):
        for line in self:
            line.tax_amount = 0.0
            if line.tax_id:
                line_tax_amount = 0.0
                if line.product_uom_qty and line.price_unit:
                    for tax_rec in line.tax_id:
                        tax = tax_rec.amount
                        tax_on_amount = (line.product_uom_qty * line.price_unit) * tax / 100
                        line_tax_amount += tax_on_amount

                line.tax_amount = line_tax_amount


class tax_on_line(models.Model):
    _inherit="account.move.line"
  
    tax_amount = fields.Monetary(string='Tax amount', store=True, readonly=True,compute="get_line_tax_amount")
    
    @api.depends('quantity','tax_ids','price_unit')
    def get_line_tax_amount(self):
        for line in self:
            line.tax_amount =0.0
            if line.tax_ids:
                line_tax_amount= 0.0
                if line.quantity and line.price_unit:
                    for tax_rec in line.tax_ids:
                        tax = tax_rec.amount
                        tax_on_amount= (line.quantity * line.price_unit) *tax/100
                        line_tax_amount += tax_on_amount
                        
                line.tax_amount = line_tax_amount  
