# -*- coding: utf-8 -*-
from odoo import api, models
from datetime import date,timedelta,datetime

class SalePersonWiseReportCustom(models.AbstractModel):
    _name = 'report.so_teamwise_report.report_teamwise_so_document'

    def get_users_sales(self,salePerson,date_from,date_to):
        # sales =self.env['sale.order'].search([('user_id','=',salePerson.id),
        #                                       ('date_order','>=',date_from),
        #                                       ('date_order','<=',date_to),
        #                                       ('state', '=', 'sale')
        #                                       ])
        sales = self.env['sale.order.line'].search([('salesman_id', '=', salePerson.id),
                                               ('order_id.date_order', '>=', date_from),
                                               ('order_id.date_order', '<=', date_to),
                                               ('order_id.state', '=', 'sale')
                                               ])
        return sales

    def get_active_users(self,wiz_partners):
       sale_orders = self.env['sale.order'].search([('user_id', 'in', wiz_partners.ids)])
       salepersons = sale_orders.mapped('user_id')
       return salepersons

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        date_from = rec_model.date_from.strftime('%b %d,%Y')
        date_to = rec_model.date_to.strftime('%b %d,%Y')
        so_team = self.get_active_users(rec_model.saleperson_ids)

        return {
            'doc_ids': self.ids,
            'date_from': date_from,
            'date_to': date_to,
            'doc_model': rec_model,
            'data': data['form'],
            'salepersons':so_team,
            'get_users_sales':self.get_users_sales
        }