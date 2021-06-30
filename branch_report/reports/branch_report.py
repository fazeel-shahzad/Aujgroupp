# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import datetime
from datetime import datetime, timedelta






class ReportAccountHashIntegrity(models.AbstractModel):
    _name = 'report.branch_report.branch_report_id'
    _description = 'Get hash integrity result as PDF.'

    # @api.model
    # def _get_report_values(self, docids, data=None, DATETIME_FORMAT=None):
    #     date_from = data['form']['date_from']
    #     date_to = data['form']['date_to']
    #     selected_id = data['form']['branch']
    #
    #     # SO = self.env['account.payment']
    #     # date_from = datetime.strptime(date_from)
    #     # start_date = datetime.strptime(date_start, DATE_FORMAT)
    #     # date_to = datetime.strptime(date_to)
    #     delta = timedelta(days=1)
    #
    #     total_values = []
    #     # while date_from <= date_to:
    #     #     date = date_from
    #     # date_from += delta
    #
    #     # print(date, date_from)
    #     # orders = self.env['account.payment'].search([('branch_id.id', '=', selected_id)])
    #     orders = self.env['account.payment'].search([])
    #     # orders = SO.search([('date', '>=', date_from.strftime(DATETIME_FORMAT)), ('date', '<', date_to.strftime(DATETIME_FORMAT)),  ('branch_id.id', '=', selected_id)
    #
    #     total_orders = len(orders)
    #     amount_total = sum(order.amount for order in orders)
    #
    #     total_values.append({
    #         # 'date': date.strftime("%Y-%m-%d"),
    #         # 'date': date.strftime("%Y-%m-%d"),
    #         # 'total_orders': total_orders,
    #         'amount_total': amount_total,
    #         'company': self.env.user.company_id
    #     })
    #
    #     return {
    #         'doc_ids': data['ids'],
    #         'doc_model': 'account.payment',
    #         'date_from': date_from,
    #         'date_to': date_to,
    #         'docs': total_values,
    #     }
    def calc_total_dbt_crd(self,vals, dbt=True):
        lst_db = []
        lst_cr = []
        total_debit =0.0
        total_credit=0.0
        if dbt == True:
            for dbt_rec in vals:
                if dbt_rec.debit:
                    lst_db.append(dbt_rec.debit)
                else:
                    lst_db.append(0.0)

            for tot_deb in lst_db:
                total_debit = total_debit + tot_deb
            tot_debit = int(round(total_debit))
            return  tot_debit


        if dbt == False:
            for crdt_rec in vals:
                if crdt_rec.credit:
                    lst_cr.append(crdt_rec.credit)
                else:
                    lst_cr.append(0.0)

            for tot_cr in lst_cr:
                total_credit = total_credit + tot_cr

            tot_credit = int(round(total_credit))
            return tot_credit





    def calc_total_balance(self, cus_mod):
        lst_db = []
        lst_cr = []
        total_debit = 0.0
        total_credit = 0.0

        for crdbt in cus_mod:
            if crdbt.debit:
                lst_db.append(crdbt.debit)
            else:
                lst_db.append(0.0)

            if crdbt.credit:
                lst_cr.append(crdbt.credit)

            else:
                lst_cr.append(0.0)

        for tot_deb in lst_db:
            total_debit = total_debit + tot_deb

        tot_debit = int(round(total_debit))

        for tot_cr in lst_cr:
            total_credit = total_credit + tot_cr

        tot_credit = int(round(total_credit))

        total_bal = tot_debit - tot_credit

        return total_bal

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        selected_id = data['form']['branch'][-3]
        print("Data", data)
        # c = selected_id[0]
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        all_val = self.env['account.payment'].search([])
        c = []

        # for i in all_val:
        #     c.append({
        #         "partner_type": i.partner_type,
        #     })
        # d = c['partner_type'] = 'customer'
        # e = d

        all_payment = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id),  ('state', '=', 'posted'),('move_type', '=', 'entry')])
        branch_name = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to),  ('state', '=', 'posted'),('branch_id.id', '=', selected_id)], limit=1)
        customer_type = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id),  ('state', '=', 'posted'),('partner_type','=', 'customer')])
        customer_type_vendor = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('state', '=', 'posted'),('branch_id.id', '=', selected_id),('partner_type','=', 'supplier')])
        customer_method = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to),  ('state', '=', 'posted'),('branch_id.id', '=', selected_id),('payment_method_id', '=', 'Checks')])
        curncy_note = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to),  ('state', '=', 'posted'),('branch_id.id', '=', selected_id),('partner_id.ceo_currency_check','=',True)])
        account_move_line = self.env['account.move'].search([('date', '>=', date_from),('date', '<=', date_to),('journal_id', '=', 'Miscellaneous Operations'),('branch_id.id', '=', selected_id),('state', '=', 'posted')])
        # account_move_line = self.env['account.move'].search([('journal_id', '=', 'Miscellaneous Operations')])
        account_line = []
        account_line1 = []

        account_move_line_data = self.env['account.move.line'].search([('date', '>=', date_from),('date', '<=', date_to),('journal_id.name', '=', 'Miscellaneous Operations'),('move_id.branch_id.id', '=', selected_id),('move_id.state', '=', 'posted')])

        # for opening balance of accounts with type 'bank and cash'

        all_acc_open_bal=0.0
        acc_bals=[]
        cash_bank_acc = self.env['account.account'].search([('user_type_id.name', '=', 'Bank and Cash')])
        for res_acc in cash_bank_acc:
            acc_jr_item = self.env['account.move.line'].search([('account_id','=',res_acc.id),('date', '<', date_from),('branch_id.id', '=', selected_id),('move_id.state', '=', 'posted')])

            acc_bal = self.calc_total_balance(acc_jr_item)
            all_acc_open_bal = all_acc_open_bal + acc_bal
            acc_bals.append({
                res_acc.name : acc_bal
            })
            acc_bal =0.0
        #end of for opening balance of accounts with type 'bank and cash'

       # all account debit(type [cash and bank])  for wizard date range
        acc_wise_bal_lst = []

        for cb_acnt in cash_bank_acc:
            acc_data = self.env['account.move.line'].search(
                [('account_id', '=', cb_acnt.id), ('date', '>=', date_from), ('date', '<=', date_to),
                 ('branch_id.id', '=', selected_id), ('move_id.state', '=', 'posted')])


            partnr_name = ''
            account_name = ''
            for rec in acc_data:
                # account_name = cb_acnt.name
                dbt = 0.0
                val_updated= False
                if rec.debit:
                    dbt = rec.debit
                # if rec.partner_id:
                #     partnr_name= rec.partner_id.name
                for awbl in acc_wise_bal_lst:

                    if rec.partner_id:
                        if rec.partner_id.id == awbl['partner_id'] and awbl['account_id'] == cb_acnt.id:

                            awbl['debit'] = awbl['debit'] + dbt
                            val_updated = True
                else:
                    if val_updated == False:

                        acc_wise_bal_lst.append({
                            'partner_id': rec.partner_id.id,
                            'account_id' : cb_acnt.id,
                            'acc_partner_name': (rec.partner_id.name if rec.partner_id.name else "") + '[' + cb_acnt.name + ']',
                            'acc_name': cb_acnt.name,
                            'debit': dbt
                        })
                # ac_total_debit=self.calc_total_dbt_crd(acc_data,True)
                # acc_wise_bal_lst.append({
                #     res_acc.name :ac_total_debit
                # })








        acc_data=[]

        for dt in account_move_line_data:
            val_updated = False
            if dt.account_id.name == 'Refreshment':
                s=''
            for acc in acc_data:
                ac_id= acc['acc_id']
                nm= acc['name']
                bal = acc['bal']
                if ac_id == dt.account_id.id:
                    acount_total_bal =  self.calc_total_balance(dt)
                    acc['bal'] = acc['bal']+acount_total_bal
                    val_updated = True


            else:
                if val_updated == False:
                    acc_total_balance= self.calc_total_balance(dt)
                    acc_data.append({
                        'acc_id':dt.account_id.id,
                        'name'  : dt.account_id.name,
                        'bal'   : acc_total_balance
                    })


        # name = account_line[]
        for i in account_move_line.line_ids:
            debit = i.debit
            c = debit
            if debit==0.0:
                account_line1.append({
                    'name': i.account_id.name,
                    'debit': i.debit,
                })
            else:
                account_line.append({
                    'name': i.account_id.name,
                    'debit': i.debit,
                })

        keys = []
        for i in account_line:
            for key in i.keys():
                keys.append(key)
        # zero = []
        # non_zero = []
        # for i in account_line[1]:
        #     if i==0:
        #         zero.append({
        #             'name': i.account_id.name,
        #             'debit': i.debit,
        #         })
        #     else:
        #         non_zero.append({
        #             'name': i.account_id.name,
        #             'debit': i.debit,
        #         })
        all_payment1 = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'out_invoice')])
        out_refund = self.env['account.move'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'out_refund')])
        all_payment_2 = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'in_invoice')])
        purchase_receipt = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'in_receipt')])
        # stock_move = self.env['stock.picking'].search([('date_done', '>=', date_from),('date_done', '<=', date_to), ('branch_id.id', '=', selected_id.id)])
        # all_payment = self.env['account.payment'].search([('branch_id.id', '=', selected_id)])

        out_refund_list = []

        for i in out_refund:
            out_refund_list.append({
                "partner_id": i.partner_id.name,
                "amount": i.amount_total,
                # "payment_type": i.payment_type,
                # "journal_id": i.journal_id,
                # "journal_id_name": i.journal_id.name,
                # "journal_name": i.journal_id.name,
                # "partner_type": i.partner_type,
                # 'branch_id': i.branch_id.id
            })

        branch_name = branch_name.branch_id.name
        d = purchase_receipt
        customer_method_list = []
        for i in customer_method:
            customer_method_list.append({
                "partner_id": i.partner_id.name,
                "amount": i.amount,
                "payment_type": i.payment_type,
                "journal_id": i.journal_id,
                "journal_id_name": i.journal_id.name,
                "journal_name": i.journal_id.name,
                "partner_type": i.partner_type,
                'branch_id': i.branch_id.id
            })
        customer_vendor_list = []
        for customer in customer_type_vendor:
            customer_vendor_list.append({
                "partner_id": customer.partner_id.name,
                "amount": customer.amount,
                "payment_type": customer.payment_type,
                "journal_id": customer.journal_id,
                "journal_name": customer.journal_id.name,
                "partner_type": customer.partner_type,
                'branch_id': customer.branch_id.id
            })

        customer_list = []
        for customer in customer_type:
            customer_list.append({
                "partner_id": customer.partner_id.name,
                "amount": customer.amount,
                "payment_type": customer.payment_type,
                "journal_id": customer.journal_id,
                "journal_name": customer.journal_id.name,
                "partner_type": customer.partner_type,
                'branch_id': customer.branch_id.id,
                'branch_name': customer.branch_id.name,
            })

        total_values = []
        for i in all_payment:
            total_values.append({
                "partner_id": i.partner_id.name,
                "amount": i.amount,
                "payment_type":i.payment_type,
                "journal_id":i.journal_id,
                "partner_type": i.partner_type,
                'branch_id': i.branch_id.id
            })


        five_th_notes=0
        one_th_notes =0
        five_hndrd_notes =0
        for note in curncy_note:
            five_th_notes = five_th_notes + note.five_th
            one_th_notes   = one_th_notes  + note.one_th
            five_hndrd_notes  = five_hndrd_notes + note.five_hundred


        return {
            'doc_ids': docids,
            'doc_model': 'account.payment',
            'data': data,
            'docs': docs,
            'total_values': total_values,
            'customer_list': customer_list,
            'customer_vendor_list': customer_vendor_list,
            'branch_name': branch_name,
            'customer_method_list': customer_method_list,
            'account_line': account_line,
            'out_refund_list': out_refund_list,
            'acc_total_list':acc_data,
            'fivth_notes' :five_th_notes,
            'oneth_note' :one_th_notes,
            'five_hndrd' : five_hndrd_notes,
            'all_acc_ob':all_acc_open_bal,
            'acc_debits':acc_wise_bal_lst

        }
# class pivotSaleReportorder(models.Model):
#     _inherit= "sale.order"
#
#     # city= fields.Char('City',readonly=True)
#     city1 = fields.Char('City1')

# class pivotSaleReport(models.Model):
#     _inherit= "sale.report"
#
#     po = fields.Many2one('purchase.order', 'po', readonly=True)
#
#     def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
#         fields['po'] = ", s.po as po"
#         groupby += ', s.po'
#         return super(pivotSaleReport, self)._query(with_clause, fields, groupby, from_clause)

    # city= fields.Char('City',readonly=True)


    # cont=
    # def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
    #     fields['city1'] = ", s.city1 as city1"
    #     groupby += ', s.city1'
    #     return super(pivotSaleReport, self)._query(with_clause, fields, groupby, from_clause)
#
#     # def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
#     #     fields['city'] = ", l.city as city_id"
#     #     groupby += ', s.city'
#     #     return super(pivotSaleReport, self)._query(with_clause, fields, groupby, from_clause)


    # def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
    #     with_ = ("WITH %s" % with_clause) if with_clause else ""
    #
    #     select_ = """
    #         coalesce(min(l.id), -s.id) as id,
    #         l.product_id as product_id,
    #         t.uom_id as product_uom,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as product_uom_qty,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_delivered / u.factor * u2.factor) ELSE 0 END as qty_delivered,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_invoiced / u.factor * u2.factor) ELSE 0 END as qty_invoiced,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.qty_to_invoice / u.factor * u2.factor) ELSE 0 END as qty_to_invoice,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.price_total / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as price_total,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as price_subtotal,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as untaxed_amount_to_invoice,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) ELSE 0 END as untaxed_amount_invoiced,
    #         count(*) as nbr,
    #         s.name as name,
    #         s.city1 as city,
    #         s.date_order as date,
    #         s.state as state,
    #         s.partner_id as partner_id,
    #         s.user_id as user_id,
    #         s.company_id as company_id,
    #         s.campaign_id as campaign_id,
    #         s.medium_id as medium_id,
    #         s.source_id as source_id,
    #         extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
    #         t.categ_id as categ_id,
    #         s.pricelist_id as pricelist_id,
    #         s.analytic_account_id as analytic_account_id,
    #         s.team_id as team_id,
    #         p.product_tmpl_id,
    #         partner.country_id as country_id,
    #         partner.industry_id as industry_id,
    #         partner.commercial_partner_id as commercial_partner_id,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(p.weight * l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as weight,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum(p.volume * l.product_uom_qty / u.factor * u2.factor) ELSE 0 END as volume,
    #         l.discount as discount,
    #         CASE WHEN l.product_id IS NOT NULL THEN sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END))ELSE 0 END as discount_amount,
    #         s.id as order_id
    #     """
    #
    #     for field in fields.values():
    #         select_ += field
    #
    #     from_ = """
    #             sale_order_line l
    #                   right outer join sale_order s on (s.id=l.order_id)
    #                   join res_partner partner on s.partner_id = partner.id
    #                     left join product_product p on (l.product_id=p.id)
    #                         left join product_template t on (p.product_tmpl_id=t.id)
    #                 left join uom_uom u on (u.id=l.product_uom)
    #                 left join uom_uom u2 on (u2.id=t.uom_id)
    #                 left join product_pricelist pp on (s.pricelist_id = pp.id)
    #             %s
    #     """ % from_clause
    #
    #     groupby_ = """
    #         l.product_id,
    #         l.order_id,
    #         t.uom_id,
    #         t.categ_id,
    #         s.name,
    #         s.date_order,
    #         s.partner_id,
    #         s.user_id,
    #         s.state,
    #         s.company_id,
    #         s.campaign_id,
    #         s.medium_id,
    #         s.source_id,
    #         s.pricelist_id,
    #         s.analytic_account_id,
    #         s.team_id,
    #         p.product_tmpl_id,
    #         partner.country_id,
    #         partner.industry_id,
    #         partner.commercial_partner_id,
    #         l.discount,
    #         s.city1,
    #         s.id %s
    #     """ % (groupby)
    #
    #     return '%s (SELECT %s FROM %s GROUP BY %s)' % (with_, select_, from_, groupby_)
