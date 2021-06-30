# -*- coding: utf-8 -*-
from odoo import api, models


class SaleReportCustom(models.AbstractModel):
    _name = 'report.sale_customer_report_pdf.report_sale_customer_document'

    def get_partner_sales(self, partner):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        records = self.env['sale.order'].search([('date_order', '>', rec_model.date_from),
                                                ('date_order', '<', rec_model.date_to), ('state', '=', 'sale'),
                                                 ('partner_id', '=', partner.id)])
        sale_list = []
        for rec in records:
            for line in rec.order_line:
                products = self.env['sale.order.line'].search([('order_id.date_order', '>', rec_model.date_from),
                                                              ('order_id.date_order', '<', rec_model.date_to),
                                                              ('order_id.partner_id', '=', partner.id),
                                                               ('product_id', '=', line.product_id.id)])
                if products[0].id not in sale_list:
                    sale_list.append(products[0].id)

        sales = self.env['sale.order.line'].browse(sale_list)
        return sales

    def get_qty(self, product, partner):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        products = self.env['sale.order.line'].search([('order_id.date_order', '>', rec_model.date_from),
                                                       ('order_id.date_order', '<', rec_model.date_to),
                                                       ('order_id.partner_id', '=', partner.id),
                                                       ('product_id', '=', product.id)])
        total_qty = 0
        for rec in products:
            total_qty = total_qty + rec.product_uom_qty
        return total_qty

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        records = self.env['sale.order'].search([('date_order', '>', rec_model.date_from),
                                                 ('date_order', '<', rec_model.date_to), ('state', '=', 'sale')])
        partner_list = []
        for i in records:
            if i.partner_id:
                partner_list.append(i.partner_id.id)
        partner_list = list(dict.fromkeys(partner_list))
        partner_ids = self.env['res.partner'].browse(partner_list)
        currencies = self.env['res.currency'].search([('name', '=', 'PKR')], limit=1)
        return {
            'doc_ids': self.ids,
            'doc_model': 'sale_customer_report_pdf.sale.customer.report.wizard',
            'partner_sales': self.get_partner_sales,
            'partner_ids': partner_ids,
            'qty': self.get_qty,
            'date_from': rec_model.date_from.date(),
            'date_to': rec_model.date_to.date(),
            'currency': currencies,
        }
