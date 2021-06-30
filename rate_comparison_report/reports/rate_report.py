from  odoo import  models,fields,api,_
from datetime import datetime,timedelta,date,time
from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
# import pandas as pd
import calendar

class RateCompReport(models.AbstractModel):
    _name = 'report.rate_comparison_report.rate_report'

    def month_last_data(self,month,sorted_po_product_lines ,product):
        try:
            date_obj= datetime.strptime(month ,"%b-%Y")
            month_fday = date_obj + relativedelta(day=1)
            month_lday = date_obj + relativedelta(day = calendar.monthrange(date_obj.year, date_obj.month)[1])
            month_lday = month_lday + timedelta(days=1)
            prd_rec = sorted_po_product_lines.filtered(lambda p : p.product_id.id == product.id)
            val_list=[]
            if prd_rec:
                for p in prd_rec:
                    if p.order_id.date_order >= month_fday and p.order_id.date_order <  month_lday:
                        val_list.append(p)
                # [x.id for x in val_list]
                if len(val_list) >=1:
                    val_list.sort(key=lambda q:q.order_id.date_order)
                    latest_prd_record= val_list[-1]
                    return  latest_prd_record
                return False
            return False
            # new_recs=prd_rec.filtered(lambda dt:dt.order_id.date_order >= month_fday and dt.order_id.date_order <= month_fday)
        except Exception as e:
            print(e)

    def get_product_latest_record(self,product, vend_po_lines):
        latest_data=[]
        po_product_lines = vend_po_lines.filtered(lambda p: p.product_id.id == product.id)
        sorted_po_product_lines =po_product_lines.sorted(key=lambda p:p.order_id.date_order)
        # latest_prd_rec = sorted_po_product_lines[-1]
        # latest_data.append(latest_prd_rec.price_unit)
        # formatted_date=(latest_prd_rec.order_id.date_order).strftime("%b-%Y")
        # latest_data.append(formatted_date)

        #return latest_data
        return sorted_po_product_lines


    def get_vendor_products(self,vend,po_lines_rec):
        vendor_po_line= po_lines_rec.filtered(lambda r:r.order_id.partner_id.id == vend.id)
        vend_products= vendor_po_line.mapped('product_id')
        return list((vend_products,vendor_po_line))






    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        month_list=[]
        date_from = rec_model.date_from.strftime('%b %d,%Y')
        date_to = rec_model.date_to.strftime('%b %d,%Y')

        date_diff= rec_model.date_to - rec_model.date_from
        dt_frm = datetime.strptime(rec_model.date_from.strftime("%Y-%m"),"%Y-%m")
        dt_to = datetime.strptime(rec_model.date_to.strftime("%Y-%m"),"%Y-%m")
        # if rec_model.date_from.year < rec_model.date_from.to:

        while(dt_frm <=dt_to ):

            month_list.append(dt_frm.strftime("%b-%Y"))
            dt_frm = dt_frm + relativedelta(months=1)

        po_line_data = self.env['purchase.order.line'].search([('order_id.partner_id', 'in', rec_model.vendor_id.ids),('order_id.date_order','>=',rec_model.date_from),('order_id.date_order','<=',rec_model.date_to),('order_id.state','=','purchase')])
        po_venders= po_line_data.mapped('order_id.partner_id')
        po_recs= po_line_data.mapped('order_id')



        # pt.mapped('product_id')
        # start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
        # OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in xrange((end - start).days)).keys()

        return {
            'doc_ids': self.ids,
            'date_from': date_from,
            'date_to': date_to,
            'doc_model': rec_model,
            'data': data['form'],
            'months':month_list,
            'vendors':po_venders,
            'po_lines':po_line_data,
            'get_vendor_product':self.get_vendor_products,
            'get_latest_data':self.get_product_latest_record,
            'month_rec':self.month_last_data
        }