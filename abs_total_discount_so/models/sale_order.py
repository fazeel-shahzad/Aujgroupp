# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api,fields,models,_

#inherit SaleOrder class.
class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_total = fields.Monetary("Discount Total",compute='total_discount')

    #Count for total discount
    @api.depends('order_line.product_uom_qty','order_line.price_unit','order_line.discount')
    def total_discount(self):
        for order in self:
            total_price = 0
            discount_amount = 0
            final_discount_amount = 0
            if order:  
                for line in order.order_line:
                    if line:
                        total_price = line.product_uom_qty * line.price_unit
                        if total_price:  
                            discount_amount = total_price - line.price_subtotal
                            if discount_amount: 
                                final_discount_amount = final_discount_amount + discount_amount
                order.update({'discount_total':final_discount_amount})

