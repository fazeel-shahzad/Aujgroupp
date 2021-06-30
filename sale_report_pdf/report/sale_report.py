# -*- coding: utf-8 -*-
from odoo import api, models


class SaleReportCustom(models.AbstractModel):
    _name = 'report.sale_report_pdf.report_sale_document'

    def get_sales(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        # records = self.env['sale.order'].search([('date_order', '>', rec_model.date_from),
        #                                             ('date_order', '<', rec_model.date_to), ('state', '=', 'sale')])
        total_qty = 0
        # for rec in records:
        #     for line in rec.order_line:
        #         if line.product_id.id == product.id:
        #             total_qty = total_qty + line.product_uom_qty

        products = self.env['sale.order.line'].search([('order_id.date_order', '>', rec_model.date_from),
                                                       ('order_id.date_order', '<', rec_model.date_to),
                                                       ('product_id', '=', product.id), ('order_id.state', '=', 'sale')])
        print(products)
        for product in products:
            total_qty = total_qty + product.product_uom_qty
        return total_qty

    def get_values(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        # records = self.env['sale.order'].search([('date_order', '>', rec_model.date_from),
        #                                         ('date_order', '<', rec_model.date_to), ('state', '=', 'sale')])
        total_value = 0
        # for rec in records:
        #     for line in rec.order_line:
        #         if line.product_id.id == product.id:
        #             total_value = total_value + (line.product_uom_qty * line.price_unit)
        products = self.env['sale.order.line'].search([('order_id.date_order', '>', rec_model.date_from),
                                                       ('order_id.date_order', '<', rec_model.date_to),
                                                       ('product_id', '=', product.id), ('order_id.state', '=', 'sale')])
        print(products)
        total_qty = 0
        for line in products:
            total_qty = total_qty + line.product_uom_qty
        total_value = total_qty * product.lst_price
        return total_value

    # def get_product_name(self, product):
    #     products = self.env['sale.order.line'].search([('product_id', '=', product.id)])
    #     if products:
    #         name = products[0].name
    #     else:
    #         name = product.display_name
    #     return name

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        currencies = self.env['res.currency'].search([('name', '=', 'PKR')], limit=1)
        return {
            'doc_ids': self.ids,
            'doc_model': 'sale_report_pdf.sale.report.wizard',
            'sales': self.get_sales,
            'values': self.get_values,
            # 'product_name': self.get_product_name,
            'products': rec_model.product_ids,
            'date_from': rec_model.date_from.date(),
            'date_to': rec_model.date_to.date(),
            'currency': currencies,
        }
