# -*- coding: utf-8 -*-
from odoo import api, models
from datetime import date,timedelta,datetime

class PurchaseOrderGoodsReportCustom(models.AbstractModel):
    _name = 'report.goods_received_report.report_pogo_received_document'

    def get_vendors_pos(self,ven,po_records):
        vendors_po = po_records.filtered(lambda q: q.partner_id.id == ven.id)
        vendors_po.sorted(key=lambda q: q.date_order, reverse=True)

        return vendors_po

    def get_product_receive_qty(self,po, prod_id):
        prd_qty=0
        stock_rec=self.env['stock.picking'].search([('purchase_id','=',po.id),('state','=','done')])
        prd_qty_rec =  stock_rec.move_ids_without_package.filtered(lambda r, p=prod_id: r.product_id == p)
        # for stk in stock_rec:
        #     prd_qty_rec= stk.move_ids_without_package.filtered(lambda r, p=prod_id: r.product_id == p)

        for q in prd_qty_rec:
            prd_qty = prd_qty + q.quantity_done
        return int(prd_qty)

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        date_from=rec_model.date_from.date().strftime('%b %d,%Y')
        date_to = rec_model.date_to.date().strftime('%b %d,%Y')

        po_data=self.env['purchase.order'].search([('date_order'.split(' ')[0], '>=', rec_model.date_from.date()),
                                           ('date_order'.split(' ')[0], '<=', rec_model.date_to.date()) ,('state','=','purchase')])


        vendors=po_data.mapped('partner_id')
        po_data.filtered(lambda r: r.date_order).sorted(key=lambda q: q.date_order, reverse=True)
        return {
            'doc_ids': self.ids,
            'date_from':date_from,
            'date_to':date_to,
            'doc_model': 'goods_received_report.po.goods.report.wizard',
            'data':data['form'],
            'po_data':po_data,
            'vendors':vendors,
            'get_prd_rece_qty':self.get_product_receive_qty,
            'get_vendor_purchase_order':self.get_vendors_pos
        }

