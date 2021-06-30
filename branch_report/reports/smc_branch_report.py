# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import datetime
from datetime import datetime, timedelta
class AccountMoveCredCard(models.Model):
    _inherit="account.move"

    cred_card_check=fields.Boolean("credit card", default=False)

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
        acc_wise_bal_lst1 = []
        cash_bank_acc = self.env['account.account'].search([('user_type_id.name', '=', 'Bank and Cash')])
        for res_acc in cash_bank_acc:
            acc_jr_item = self.env['account.move.line'].search([('account_id','=',res_acc.id),('date', '<', date_from),('move_id.journal_id.type','in',['cash','general']),('branch_id.id', '=', selected_id),('move_id.state', '=', 'posted')])

            acc_bal = self.calc_total_balance(acc_jr_item)
            all_acc_open_bal = all_acc_open_bal + acc_bal
            acc_bals.append({
                res_acc.name : acc_bal
            })
            acc_bal =0.0
        #end of for opening balance of accounts with type 'bank and cash'
       #test

            acc_data = self.env['account.move.line'].search(
                [('account_id', '=', res_acc.id), ('date', '>=', date_from), ('date', '<=', date_to),
                 ('branch_id.id', '=', selected_id), ('move_id.state', '=', 'posted'),('move_id.journal_id.type','=','cash')])

            for rec1 in acc_data:
                dbt1 = 0.0
                if rec1.debit:
                    dbt1 = rec1.debit

                acc_wise_bal_lst1.append({
                    'partner_id': rec1.partner_id.id,
                    'account_id': res_acc.id,
                    'acc_partner_name': (rec1.partner_id.name if rec1.partner_id.name else "") + '[' + res_acc.name + ']',
                    'acc_name': res_acc.name,
                    'debit': dbt1
                })
       #test
       # all account debit(type [cash and bank])  for wizard date range
        acc_wise_bal_lst = []

        for cb_acnt in cash_bank_acc:
            acc_data = self.env['account.move.line'].search(
                [('account_id', '=', cb_acnt.id), ('date', '>=', date_from), ('date', '<=', date_to),
                 ('branch_id.id', '=', selected_id), ('move_id.state', '=', 'posted'),('move_id.journal_id.type','=','cash')])



            for rec in acc_data:

                dbt = 0.0
                val_updated= False
                if rec.debit:
                    dbt = rec.debit
                    journal_entry = rec.move_id
                    payment = self.env['account.payment'].search([('move_id', '=', journal_entry.id),
                                                                  ('state', '=', 'posted'),
                                                                  ('date', '>=', date_from),
                                                                  ('date', '<=', date_to),
                                                                  ('branch_id.id', '=',selected_id ),
                                                                  ])

                    if payment:
                        if payment.corporate_sale == False and payment.other_receipt == False and payment.cheques_payment == False and payment.online_credit_payment == False:
                            acc_wise_bal_lst.append({
                                'partner_journal': (rec.partner_id.name if rec.partner_id.name else "") + '[' + rec.journal_id.name + ']',
                                'debit': dbt,
                            })





                    # cred_acc_rec= self.env['account.move.line'].search(
                    #     [('date', '>=', date_from), ('date', '<=', date_to), ('branch_id.id', '=', selected_id),
                    #      ('move_id', '=', rec.move_id.id), ('move_id.state', '=', 'posted')])
                    # if cred_acc_rec:
                    #     cred_acnt=cred_acc_rec.filtered(lambda r: r.credit == rec.debit)
                    #     acc_wise_bal_lst.append({
                    #                     # 'partner_id': rec.partner_id.id,
                    #                     'account_id' : cb_acnt.id,
                    #                     # 'acc_partner_name': (rec.partner_id.name if rec.partner_id.name else "") + '[' + cb_acnt.name + ']',
                    #                     'acc_name': cb_acnt.name,
                    #                     'debit': dbt,
                    #                     'cred_acnt':cred_acnt.account_id.name,
                    #                     'partner_journal':(rec.partner_id.name if rec.partner_id.name else "") + '['+rec.journal_id.name+']'
                    #                 })


        if len(acc_wise_bal_lst) > 0:
            acc_wise_bal_lst =[i for i in acc_wise_bal_lst if not (i['debit'] == 0.0)]

        #for showroom expenses calculating accounts'type cash and bank' credit values
        # ajitem-----> account Journal items
        acc_data = []
        acc_crd_list=[]
        for cr_accnts in cash_bank_acc:
            ajitem =self.env['account.move.line'].search(
                [('account_id', '=', cr_accnts.id), ('date', '>=', date_from), ('date', '<=', date_to),
                 ('branch_id.id', '=', selected_id), ('move_id.state', '=', 'posted'),('move_id.journal_id.type', 'in',  ['cash','general'])])


            for crdit_record in ajitem:
                cre_val=0.0
                if crdit_record.credit:
                    cre_val = crdit_record.credit
                    cr_jv= crdit_record.move_id
                    jornal_entry= self.env['account.move.line'].search([('date', '>=', date_from),
                                                                        ('date', '<=', date_to),
                                                                        ('branch_id.id', '=', selected_id),
                                                                        ('move_id.state', '=', 'posted'),
                                                                        ('move_id.id','=',cr_jv.id),('move_id.journal_id.type', 'in', ['cash','general'])])

                    rec_debt = jornal_entry.filtered(lambda r:r.debit == cre_val)
                    # if rec_debt.account_id.user_type_id.name != 'Payable' and rec_debt.account_id.user_type_id.name != 'Receivable':
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Expenses':
                            acc_crd_list.append({
                                  'name': rec_debt.account_id.name,
                                  'credit' : cre_val,
                                  'cred_acc': crdit_record.account_id.name,
                                  'partner':  crdit_record.partner_id.name
                            })
    # all accounts(type 'cash and bank')'s credit vals [account wise combined]
        #     for dt in ajitem:
        #         val_updated = False
        #
        #         for acc in acc_data:
        #             ac_id= acc['acc_id']
        #             nm= acc['name']
        #             bal = acc['bal']
        #             if ac_id == dt.account_id.id:
        #                 acount_total_bal =   self.calc_total_dbt_crd(dt,False)
        #                 acc['bal'] = acc['bal']+acount_total_bal
        #                 val_updated = True
        #
        #
        #         else:
        #             if val_updated == False:
        #                 acc_total_balance= self.calc_total_dbt_crd(dt,False)
        #                 acc_data.append({
        #                     'acc_id':dt.account_id.id,
        #                     'name'  : dt.account_id.name,
        #                     'bal'   : acc_total_balance
        #                 })
    #end  all accounts(type 'cash and bank')'s credit vals [account wise combined]
        # # for showroom expenses calculating accounts'type cash and bank' credit values

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
        # for purchase column
        purchases_list=[]
        # cash_bank_acc = self.env['account.account'].search([('user_type_id.name', '=', 'Bank and Cash')])
        # payable_acc = self.env['account.account'].search([('user_type_id.name', '=', 'Payable')])
        for pay_acc in cash_bank_acc:
            jr_item_rcs = self.env['account.move.line'].search([('account_id', '=', pay_acc.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted'),
                                                                ('move_id.journal_id.type', '=', 'cash')])
            for j_rec in jr_item_rcs:
                credt_val = 0.0
                partner_name=''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_jv = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_jv.id),
                                                                         ('move_id.journal_id.type', '=', 'cash')
                                                                         ])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Payable':

                            purchases_list.append({
                                'cre_acc':j_rec.account_id.name,
                                'partnr': partner_name,
                                'credit':credt_val,
                                'debit_acc':rec_debt.account_id.name
                            })

        # for sale column
        sale_return_list=[]
        # receiv_acc = self.env['account.account'].search([('user_type_id.name', '=', 'Receivable')])
        for recv_acc in cash_bank_acc:
            jr_item_rcs = self.env['account.move.line'].search([('account_id', '=', recv_acc.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted'),
                                                                ('move_id.journal_id.type', '=', 'cash')])
            for j_rec in jr_item_rcs:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_jv = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_jv.id),
                                                                         ('move_id.journal_id.type', '=', 'cash')])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Receivable':



                            sale_return_list.append({
                                'cre_acc': j_rec.account_id.name,
                                'partnr': partner_name,
                                'credit': credt_val,
                                'debit_acc': rec_debt.account_id.name
                            })

        # for Online Payments & Cross Cheques
        cheq_payment_list=[]
        for accnt in cash_bank_acc:
            jr_item_rcs = self.env['account.move.line'].search([('account_id', '=', accnt.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted')])
            for j_rec in jr_item_rcs:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_jv = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         # ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_jv.id)])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        payment_entr = self.env['account.payment'].search(
                            [('state', '=', 'posted'), ('move_id', '=', 'rec_debt.move_id.id')])
                        if payment_entr:
                            if payment_entr.payment_method_id.name == 'Online and Cheque':
                                if rec_debt[0].account_id.user_type_id.name == 'Bank and Cash':
                                    cheq_payment_list.append({
                                        'cre_acc': j_rec.account_id.name,
                                        'partnr': partner_name,
                                        'credit': credt_val,
                                        'debit_acc': rec_debt.account_id.name
                                    })


        # end for Online Payments & Cross Cheques
        #creditss
        credit_card_payment_list1 = []
        for accnt in cash_bank_acc:
            jr_item_rcs = self.env['account.move.line'].search([('account_id', '=', accnt.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted')])
            for j_rec in jr_item_rcs:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_jv = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         # ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_jv.id)])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)

                    if rec_debt:
                        payment_entr= self.env['account.payment'].search([('state','=','posted'),('move_id','=','rec_debt.move_id.id')])
                        if payment_entr:
                            if payment_entr.payment_method_id.name == 'Credit Card':

                                if rec_debt[0].account_id.user_type_id.name == 'Bank and Cash':
                                    credit_card_payment_list1.append({
                                        'cre_acc': j_rec.account_id.name,
                                        'partnr': partner_name,
                                        'credit': credt_val,
                                        'debit_acc': rec_debt.account_id.name
                                    })


        #for cash transfer
        cash_transfer_list=[]
        for account_rec in cash_bank_acc:
            jr_item_rcs = self.env['account.move.line'].search([('account_id', '=', account_rec.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted'),
                                                                ('move_id.journal_id.type',  'in', ['cash','general'])])
            for j_rec in jr_item_rcs:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_jv = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_jv.id),
                                                                         ('move_id.journal_id.type', 'in', ['cash','general'])])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Current Assets':



                            cash_transfer_list.append({
                                'cre_acc': j_rec.account_id.name,
                                'partnr': partner_name,
                                'credit': credt_val,
                                'debit_acc': rec_debt.account_id.name
                            })
        #end for cash transfer

        # bank sale return
        bank_sale_return_list=[]
        for account_rec in cash_bank_acc:
            journal_items = self.env['account.move.line'].search([('account_id', '=', account_rec.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted'),
                                                                ('move_id.journal_id.type', '=', 'bank')])
            for j_rec in journal_items:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_journalEntry = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_journalEntry.id),
                                                                         ('move_id.journal_id.type', '=', 'bank')])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Receivable':
                            bank_sale_return_list.append({
                                'cre_acc': j_rec.account_id.name,
                                'partnr': partner_name,
                                'credit': credt_val,
                                'debit_acc': rec_debt.account_id.name
                            })

        #end bank sale return

        #bank credit card
        bank_credit_card_list=[]
        for account_rec in cash_bank_acc:
            journal_items = self.env['account.move.line'].search([('account_id', '=', account_rec.id),
                                                                ('date', '>=', date_from),
                                                                ('date', '<=', date_to),
                                                                ('branch_id.id', '=', selected_id),
                                                                ('move_id.state', '=', 'posted'),
                                                                ('move_id.journal_id.type', '=', 'bank')])


            for j_rec in journal_items:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_journalEntry = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_journalEntry.id),
                                                                         ('move_id.journal_id.type', '=', 'bank')])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Payable':
                            credit_payment_rec = self.env['account.payment'].search([('move_id','=', j_rec.move_id.id),
                                                                                     ('state','=','posted'),
                                                                                     ('date', '>=', date_from),
                                                                                     ('date', '<=', date_to),
                                                                                     ('branch_id.id', '=', selected_id),
                                                                                     ])
                            if credit_payment_rec:
                                if credit_payment_rec.online_credit_payment == True:
                                    bank_credit_card_list.append({
                                        'cre_acc': j_rec.account_id.name,
                                        'partnr': partner_name,
                                        'credit': credt_val,
                                        'debit_acc': rec_debt.account_id.name
                                    })

        #end bank credit card
        #bank transfers
        bank_transfer_list = []
        for account_rec in cash_bank_acc:
            journal_items = self.env['account.move.line'].search([('account_id', '=', account_rec.id),
                                                                  ('date', '>=', date_from),
                                                                  ('date', '<=', date_to),
                                                                  ('branch_id.id', '=', selected_id),
                                                                  ('move_id.state', '=', 'posted'),
                                                                  ('move_id.journal_id.type', '=', 'bank')])

            for j_rec in journal_items:
                credt_val = 0.0
                partner_name = ''
                if j_rec.credit:
                    credt_val = j_rec.credit
                    if j_rec.partner_id:
                        partner_name = j_rec.partner_id.name

                    cr_journalEntry = j_rec.move_id
                    jornal_entry = self.env['account.move.line'].search([('date', '>=', date_from),
                                                                         ('date', '<=', date_to),
                                                                         ('branch_id.id', '=', selected_id),
                                                                         ('move_id.state', '=', 'posted'),
                                                                         ('move_id.id', '=', cr_journalEntry.id),
                                                                         ('move_id.journal_id.type', '=', 'bank')])

                    rec_debt = jornal_entry.filtered(lambda r: r.debit == credt_val)
                    if rec_debt:
                        if rec_debt[0].account_id.user_type_id.name == 'Current Assets':

                            bank_transfer_list.append({
                                'cre_acc': j_rec.account_id.name,
                                'partnr': partner_name,
                                'credit': credt_val,
                                'debit_acc': rec_debt.account_id.name
                            })

        #end bank transfers





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
            # 'acc_total_list':acc_data,
            'fivth_notes' :five_th_notes,
            'oneth_note' :one_th_notes,
            'five_hndrd' : five_hndrd_notes,
            'all_acc_ob':all_acc_open_bal,
            'acc_debits':acc_wise_bal_lst,
            'acc_credits':acc_crd_list,
            'purchase_data':purchases_list,
            'sale_return_data':sale_return_list,
            'cash_transfer_data':cash_transfer_list,
            'cheq_payment':cheq_payment_list,
            'cheq_payment1' :credit_card_payment_list1,
            'bank_sale_return':bank_sale_return_list,
            'bank_credit_card':bank_credit_card_list,
            'bank_transfer':bank_transfer_list,
            'credit_check': self.get_credit_cheques_accounts,
            'credit_online': self.get_credit_online_accounts,
            'cash_corporate_receipt': self.get_corporateSale_otherReceipt

        }

    def get_credit_online_accounts(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        account_type = self.env['account.account.type'].search([('name', '=', 'Bank and Cash')])
        accounts = self.env['account.account'].search([('user_type_id', '=', account_type.id)])
        account_list = []

        journal_items = self.env['account.move.line'].search([('journal_id.type', '=', 'bank'),
                                                              ('date', '>=', rec_model.date_from),
                                                              ('date', '<=', rec_model.date_to)])
        for rec in journal_items:
            if rec.account_id.user_type_id.name == 'Bank and Cash':

                creditobj = self.env['account.move.line'].search([('move_id', '=', rec.move_id.id), ('credit', '>', 0),('branch_id', '=',rec_model.branch.id)])
                paymentobj = self.env['account.payment'].search(
                    [('move_id', '=', rec.move_id.id), ('online_credit_payment', '=', True)])
                if paymentobj.branch_id.id == rec_model.branch.id and rec.debit > 0:
                    print(creditobj.name)
                    account_list.append({
                              'name': str(creditobj.partner_id.name) + ' ' + "("+str(creditobj.journal_id.name)+")",
                        'debit': rec.debit
                    })
        return account_list

    def get_credit_cheques_accounts(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        account_type = self.env['account.account.type'].search([('name', '=', 'Bank and Cash')])
        accounts = self.env['account.account'].search([('user_type_id', '=', account_type.id)])
        account_list = []

        journal_items = self.env['account.move.line'].search([('journal_id.type', '=', 'bank'),
                                                              ('date', '>=', rec_model.date_from),
                                                              ('date', '<=', rec_model.date_to)])
        for rec in journal_items:
            if rec.account_id.user_type_id.name == 'Bank and Cash':
                print(rec.move_id.ref)

                creditobj = self.env['account.move.line'].search([('move_id', '=', rec.move_id.id), ('credit', '>', 0),('branch_id', '=',rec_model.branch.id)])
                paymentobj = self.env['account.payment'].search(
                    [('move_id', '=', rec.move_id.id), ('cheques_payment', '=', True)])
                if paymentobj.branch_id.id == rec_model.branch.id and rec.debit > 0:
                    print(creditobj.name)
                    account_list.append({
                        'name': str(creditobj.partner_id.name) + ' ' + "(" + str(creditobj.journal_id.name) + ")",
                        'debit': rec.debit
                    })
        return account_list

    def get_corporateSale_otherReceipt(self, corporate=False, receipt=False , cash=False , bank= False):
        corporate_sale_list= []
        other_receipt_list  =[]

        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        cash_bank_acc = self.env['account.account'].search([('user_type_id.name', '=', 'Bank and Cash')])


        for cb_account in cash_bank_acc:
            if cash == True:
                journal_items = self.env['account.move.line'].search([('account_id', '=', cb_account.id),
                                                                        ('date', '>=', rec_model.date_from),
                                                                        ('date', '<=', rec_model.date_to),
                                                                        ('branch_id.id', '=', rec_model.branch.id),
                                                                        ('move_id.state', '=', 'posted'),
                                                                        ('move_id.journal_id.type', '=', 'cash')])
            if bank == True:
                journal_items = self.env['account.move.line'].search([('account_id', '=', cb_account.id),
                                                                      ('date', '>=', rec_model.date_from),
                                                                      ('date', '<=', rec_model.date_to),
                                                                      ('branch_id.id', '=', rec_model.branch.id),
                                                                      ('move_id.state', '=', 'posted'),
                                                                      ('move_id.journal_id.type', '=', 'bank')])

            for rec in journal_items:
                if rec.debit:
                    dbt = rec.debit
                    journal_entry= rec.move_id
                    payment = self.env['account.payment'].search([('move_id', '=', journal_entry.id),
                                                                             ('state', '=', 'posted'),
                                                                             ('date', '>=', rec_model.date_from),
                                                                             ('date', '<=', rec_model.date_to),
                                                                             ('branch_id.id', '=', rec_model.branch.id),
                                                                             ])

                    if payment:
                        if payment.corporate_sale == True:
                            corporate_sale_list.append({
                                'name': (rec.partner_id.name if rec.partner_id.name else "") + '[' + rec.journal_id.name + ']',
                                'debit': dbt
                            })


                        if payment.other_receipt == True:
                            other_receipt_list.append({
                                'name': (rec.partner_id.name if rec.partner_id.name else "") + '[' + rec.journal_id.name + ']',
                                'debit': dbt
                            })

        if(corporate == True):
            return corporate_sale_list
        if (receipt == True):
            return other_receipt_list
