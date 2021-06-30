from odoo import models, fields, api, _, exceptions
from datetime import datetime, timezone
import urllib.parse
from requests import request
from dateutil import parser
import urllib.parse
from hashlib import sha256
from hmac import HMAC
import json
import urllib.request



class TransactionDetail(models.Model):
    _name = 'transaction.detail'
    _order = 'id desc'
    _description = "Transaction Detail"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Transaction Number')
    instance_id = fields.Many2one('daraz.connector', "Daraz Store")
    comments = fields.Text("Comments")
    invoice_id = fields.Many2one('account.move', "Invoice")
    sale_id = fields.Many2one('sale.order', "Sale Order")
    trans_date = fields.Date('Transaction Date')
    trans_ttype = fields.Char('Transaction Type')
    amount = fields.Float('Amount')
    wht_incl = fields.Boolean('WHT included in Amount')
    statement = fields.Char('Statement')
    paid_status = fields.Boolean('Paid Status')
    order_no = fields.Char('Order No.')
    order_item_no = fields.Char('Order Item No.')
    ship_ttype = fields.Char('Shipment Type')
    reference = fields.Char('Reference')
    payment_fee = fields.Char('Payment Fee')
    fee_name = fields.Char('Fee Name')
    company_id = fields.Many2one('res.company', string='Company')
    invoice_status = fields.Boolean('Invoice Status')


    def set_so_in_trans(self, instance, job=False):
        if not job:
            job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'import',
                 'message': 'Set SO in transaction'})
        recs = self.search([('sale_id','=', False),('instance_id','=', instance.id)])
        for rec in recs:
            so_id = self.env['sale.order'].search([('orderid','=', rec.order_no)], limit=1)
            if so_id:
                rec.write({'sale_id': so_id.id})
        return True

    def import_transactions(self, instance, job=False):

        if not job:
            job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'import',
                 'message': 'Process for import transaction'})

        # res = self.connect_with_store('GetTransactionDetails', 'GET', instance_id=instance, extra_parameters={'endTime': str(fields.Date.today()), 'maxItem': 300, 'startTime': '2017-01-01', 'transType':-1})
        # result = res and res.get('SuccessResponse', {}).get('Body', {}).get('TransactionDOs', {}).get('transactionDOs', {}) or {}

        # for val in result:
        #     trans_no = val.get('Transaction Number')
        #     if self.search([('name', '=', trans_no)]):
        #         continue
        #     date = val.get('Transaction Date', False)
        #     trans_type = val.get('Transaction Type', '')
        #     amt = val.get("Amount", 0.00)
        #     wht_val = val.get("WHT included in Amount", False)
        #     statement = val.get("Statement", '')
        #     paid_status_val = val.get("Paid Status", '')
        #     order_no = val.get("Order No.", '')
        #     order_item_no = val.get("Order Item No.", '')
        #     ship_type = val.get("Shipment Type", '')
        #     ship_provider = val.get('Shipment provider', {})
        #     if wht_val == 'Yes':
        #         wht = True
        #     else:
        #         wht = False
        #     if paid_status_val == 'Not Paid':
        #         paid_status = False
        #     else:
        #         paid_status = True
        #     so_id = self.env['sale.order'].search([('orderid','=', order_no)], limit=1)
        #     trans_date = datetime.strptime(date, '%d %b %Y')
        #     trans_rec = self.create({'name': trans_no, 'sale_id': so_id and so_id.id or False, 'trans_date': trans_date, 'instance_id': instance.id, 'trans_ttype': trans_type, 'amount': amt,
        #     'wht_incl': bool(wht), 'statement': statement, 'paid_status': paid_status, 'order_no': order_no, 'order_item_no': order_item_no, 'ship_ttype': ship_type })
        # if job:
        #     job.response = res

        flag = 0
        offset = 0
        # new_result = False
        # while(True):
        new_res = self.connect_with_store('GetTransactionDetails', 'GET', instance_id=instance, extra_parameters={'endTime': str(fields.Date.today()), 'startTime' : '2017-01-01', 'transType':-1, 'Limit': 600000, 'maxItem': 600000, 'Offset': offset})#

        new_result = new_res and new_res.get('SuccessResponse', {}).get('Body', {}).get('TransactionDOs', {}).get('transactionDOs', {}) or {}

        # offset += 301

        for val in new_result:
            trans_no = val.get('Transaction Number')
            if self.search([('name', '=', trans_no)]):
                continue
            date = val.get('Transaction Date', False)
            trans_type = val.get('Transaction Type', '')
            amt = val.get("Amount", 0.00)
            wht_val = val.get("WHT included in Amount", False)
            statement = val.get("Statement", '')
            paid_status_val = val.get("Paid Status", '')
            order_no = val.get("Order No.", '')
            order_item_no = val.get("Order Item No.", '')
            ship_type = val.get("Shipment Type", '')
            fee_name=val.get("Fee Name", '')

            ship_provider = val.get('Shipment provider', {})
            if wht_val == 'Yes':
                wht = True
            else:
                wht = False
            if paid_status_val == 'Not Paid':
                paid_status = False
            else:
                paid_status = True
            so_id = self.env['sale.order'].search([('orderid','=', order_no)], limit=1)
            trans_date = datetime.strptime(date, '%d %b %Y')
            trans_rec = self.create({'name': trans_no, 'sale_id': so_id and so_id.id or False, 'trans_date': trans_date, 'instance_id': instance.id, 'trans_ttype': trans_type, 'amount': amt,
            'wht_incl': bool(wht), 'statement': statement, 'paid_status': paid_status, 'order_no': order_no, 'order_item_no': order_item_no, 'ship_ttype': ship_type , 'fee_name': fee_name })
            flag = flag + 1
            # offset += 300
            # if not new_result:
            #     break
            #     # newresult = False
            #     print(new_result)
            #     if not oldresult :
            #         oldresult = new_result
            #     if oldresult == new_result:
            #         break

            if flag > 10:
                flag = 0
                self._cr.commit()
        # else:
        #     job.env['process.job.line'].create({'job_id': job.id, 'message': "Empty Response"})

        return True

    def connect_with_store(self, action=None, req=None, instance_id=False, extra_parameters={}, job=False):
        darazStore = instance_id
        url = darazStore.api_url
        api_key = darazStore.api_key
        format = "json"
        userId = darazStore.userId
        method = req if req else 'GET'

        test = datetime.fromtimestamp(datetime.now().timestamp(), tz=timezone.utc).replace(microsecond=0).isoformat()
        parameters = {
            'UserID': userId,
            'Version': "1.0",
            'Action': action,
            'Format': format,
            'Timestamp': test}

        if extra_parameters:
            parameters.update(extra_parameters)
        concatenated = urllib.parse.urlencode(sorted(parameters.items()))
        parameters['Signature'] = HMAC(api_key.encode('utf-8'), concatenated.encode('utf-8'),  sha256).hexdigest()
        
        headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        if job:
            job.request = concatenated
        try:

            response = request(method, url, headers=headers, params=parameters)
            if job:
                job.response = response.text
        except Exception as e:
            raise Warning(_(response.text))
        try:
            return json.loads(response.text)
        except Exception as e:
            raise Warning(_(response.text))

    @api.model
    def auto_import_transaction(self, ctx={}):
        instance_obj = self.env["daraz.connector"]
        if not isinstance(ctx, dict) or not 'instance_id' in ctx:
            return True
        instance_id = ctx.get('instance_id', False)
        instance = instance_id and instance_obj.search(
            [('id', '=', instance_id), ('state', '=', 'connected')]) or False
        if instance:
            job = self.env['process.job'].create(
            {'instance_id': instance.id, 'process_type': 'order', 'operation_type': 'import',
             'message': 'Process for Import Order'})

            self.import_transactions(instance, job)
            instance.so_import_next_execution = instance.so_import_cron_id.nextcall
        return True

    @api.model
    def auto_set_so_transaction(self, ctx={}):
        instance_obj = self.env["daraz.connector"]
        if not isinstance(ctx, dict) or not 'instance_id' in ctx:
            return True
        instance_id = ctx.get('instance_id', False)
        instance = instance_id and instance_obj.search(
            [('id', '=', instance_id), ('state', '=', 'connected')]) or False
        if instance:
            job = self.env['process.job'].create(
            {'instance_id': instance.id, 'process_type': 'order', 'operation_type': 'import',
             'message': 'Process for Import Order'})

            self.set_so_in_trans(instance, job)
            instance.so_import_next_execution = instance.so_import_cron_id.nextcall
        return True

    @api.model
    def auto_cre_inv_transaction(self, ctx={}):
        instance_obj = self.env["daraz.connector"]
        if not isinstance(ctx, dict) or not 'instance_id' in ctx:
            return True
        instance_id = ctx.get('instance_id', False)
        instance = instance_id and instance_obj.search(
            [('id', '=', instance_id), ('state', '=', 'connected')]) or False
        if instance:
            job = self.env['process.job'].create(
            {'instance_id': instance.id, 'process_type': 'order', 'operation_type': 'import',
             'message': 'Process for Import Order'})

            self.create_invoice(instance, job)
            instance.so_import_next_execution = instance.so_import_cron_id.nextcall
        return True

    def create_invoice(self):
        data_dict = {}
        for res in self:
            res.invoice_status=True
            if res.invoice_id:
                continue
            # if not res.sale_id:
            #     so_id = self.env['sale.order'].search([('orderid','=', res.order_no)], limit=1)
            #     if so_id:
            #         res.write({'sale_id': so_id.id})
            #     else:
            #         raise exceptions.UserError(_('The order is not available.'))
            account_obj = self.env['account.account']
            journal = self.env['account.move'].with_context(default_type='sale')._get_default_journal()
            if not journal:
                raise exceptions.UserError(
                    _('Please define an accounting sales journal for the company %s.'
                      ) % res.company_id.name)
            if res.sale_id not in data_dict:
                data_dict.update({res.sale_id: [res]})
                print("if,",data_dict)
            else:
                old_data = data_dict.get(res.sale_id)
                data_dict.update({res.sale_id: old_data + [res]})
                print("else",data_dict)

        for sale, rec in data_dict.items():
            data = {
                    'type': 'out_invoice',
                    'partner_id': sale.partner_id.id or False,
                    'invoice_date': str(sale.date_order),
                    'currency_id': sale.currency_id.id or False,
                    'company_id': sale.company_id.id or False,
                    'invoice_payment_term_id': sale.payment_term_id and sale.payment_term_id.id or False,
                    'invoice_user_id': sale.user_id and sale.user_id.id or False,
                    'team_id': sale.team_id and sale.team_id.id or False,
                    'invoice_origin': sale.name,
                    'narration': sale.note or '',
                    'ref': sale.client_order_ref or '',
                    'partner_shipping_id': sale.partner_shipping_id or False,
                    'invoice_line_ids': [(0, 0, {'product_id': line.product_id.id or False,
                                                 'name': line.name or '',
                                                 'quantity': 1,
                                                 'price_unit': line.price_unit,
                                                 'product_uom_id': line.product_uom.id or False,
                                                 'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                                                 'account_id': line.product_id.categ_id.property_account_income_categ_id.id or account_obj.search([('name', '=', 'Incomes')], limit=1).id,
                                                 'journal_id': journal.id,
                                                }) for line in sale.order_line],
                    }
            data.update(self.env['account.move'].default_get(['reference_type']))
            invoice = self.env['account.move'].create(data)
            invoice_vals = {}
            line_vals = []
            prices = invoice.line_ids.mapped('price_unit')

            for val in rec:
                val.invoice_id = invoice
                if val.amount in prices:
                    continue
                line_vals.append([0, 0, {'name': 'Daraz Fees' + '-' + val.name or '', 'quantity': 1,
                                  'price_unit': val.amount or 0.00, 'journal_id': journal.id}])
            invoice.write({'invoice_line_ids': line_vals})

            sale.invoice_ids = invoice
            for line in sale.order_line:
                line.write({'invoice_lines': [(4, inl.id) for inl in invoice.invoice_line_ids.filtered(lambda x: x.product_id.id == line.product_id.id)]})