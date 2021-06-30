from odoo import models, fields, api,_
from odoo.exceptions import Warning
from datetime import datetime, timezone
from requests import request
from dateutil import parser
import urllib.parse
from hashlib import sha256
from hmac import HMAC
import json
import urllib.request
import time
import base64
import time


class SaleOrder(models.Model):
    _inherit = "sale.order"

    instance_id = fields.Many2one('daraz.connector', 'Daraz Store')
    qty_on_hand = fields.Float(string="Qty On Hand", compute='get_qty_on_hand', store=True)
    type = fields.Selection([('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product'),
        ], string='Product Type', compute='get_qty_on_hand', store=True)
    update_order_status = fields.Boolean('Update Status to Daraz', help='Want to update Order status to daraz?')
    orderid = fields.Char("Daraz Order Reference", help="Daraz Order Reference")
    order_status = fields.Selection([('pending', 'Pending'),
                                     ('ready_to_ship','Ready To Ship'), 
                                     ('delivered', 'Delivered'), ('shipped','Shipped'),
                                     ('canceled', 'Cancelled'), ('returned','Returned'),
                                     ('return_waiting_for_approval','Return Waiting For Approval'), 
                                     ('return_shipped_by_customer','Return Shipped By Customer'), 
                                     ('return_rejected','Return Rejected'),
                                     ('processing','Processing'), 
                                     ('failed', 'Failed'), ('physical', 'Physically Returned'), ('ask', 'Ask for claimed'),  ('claimed', 'Claimed'),  ('received', 'Claimed Received')
                                    ],string="Daraz Order Status", track_visibility='onchange', copy=False)
    customer_name = fields.Char("Customer Name")
    doc_imported = fields.Boolean('Done with Document Import?')
    status_is_updated = fields.Boolean("Status updated?")
    shipping_provider = fields.Char('Shipping Provider')
    delivery_type = fields.Selection([('dropship', 'Dropship'), ('pickup', 'Pickup'), ('send_to_warehouse', 'Send to Warehouse')], "Delivery Type", default='dropship')
    cancel_reason = fields.Selection([('delay', 'Sourcing Delay(cannot meet deadline)'),
                                     ('out_of_stock', 'Out of Stock'), 
                                     ('wrong_price', 'Wrong Price or Pricing Error')
                                    ], string="Cancel Reason", copy=False)
    po_ids = fields.One2many('purchase.order','so_id', string='Purchase Orders', copy=False)
    po_count = fields.Integer(string='PO Count', compute='_get_po_custom', readonly=True)

    def get_qty_on_hand(self):
        for order in self:
            ttype = order.order_line and order.order_line[0].product_id.type or 'consu'
            order.type = ttype
            if ttype == 'product':
                order.qty_on_hand = order.order_line and order.order_line[0].product_id.qty_available or 0.00

    def import_document_sale_order(self, instance=False, job=False):
        self.ensure_one()
        if not instance:
            instance = self.instance_id
        if not job:
            job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})
        
        doc_type = 'shippingLabel'
        type_doc = self._context.get('doc_type')
        if type_doc:
            doc_type = type_doc

        OrderItemIds = self.order_line.mapped('item_id')
        res = self.connect_with_store('GetDocument', 'GET', instance_id=instance, extra_parameters={'OrderItemIds': json.dumps(OrderItemIds), 'DocumentType' : doc_type})
        result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
        print(result)
        if job:
            job.response = res
        if result:
            self.doc_imported = True
            val = result.get('Document')
            doc_type = val.get('DocumentType')
            mime_type = val.get('MimeType','')
            file = val.get('File')
            file_name = "Document_" + time.strftime("%Y_%m_%d_%H%M%S") + '.html'
            attachment = self.env['ir.attachment'].create({
                                               'name': file_name,
                                               'datas': file,
                                               'res_model': 'sale.order', 
                                               'res_id' : self.id,
                                              # 'type': 'binary'
                                             })

            self.message_post(body=_("<b>Document Downloaded</b>"), attachment_ids=attachment.ids)
        else:
            if job:
                job.env['process.job.line'].create({'job_id': job.id, 'message': "Empty Response"})

        return True

    def get_failure_reason(self):
        self.ensure_one()
        if not instance:
            instance = self.instance_id
        job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})
        
        # OrderItemIds = self.order_line.mapped('item_id')
        res = self.connect_with_store('GetFailureReasons', 'GET', instance_id=instance) #, extra_parameters={'OrderItemIds': json.dumps(OrderItemIds)})
        result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
        if job:
            job.response = res
        if result:
            vals = result.get('Reasons')
            doc_type = val.get('DocumentType')
            mime_type = val.get('MimeType','')
            file = val.get('File')
            file_name = "Document_" + time.strftime("%Y_%m_%d_%H%M%S") + '.html'
            attachment = self.env['ir.attachment'].create({
                                               'name': file_name,
                                               'datas': file,
                                               'res_model': 'sale.order', 
                                               'res_id' : self.id,
                                              # 'type': 'binary'
                                             })

            self.message_post(body=_("<b>Document Downloaded</b>"), attachment_ids=attachment.ids)
        else:
            if job:
                job.env['process.job.line'].create({'job_id': job.id, 'message': "Empty Response"})

        return True

    def import_docs(self, instance, job=False):
        flag = 0
        orders = self.env['sale.order'].search([('instance_id','=', instance.id), ('order_status','=','ready_to_ship'), ('doc_imported','=', False)])
        for order in orders:
            if not job:
                job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})
            order.import_document_sale_order(instance, job)
            # if result:
            if flag > 10:
                flag = 0
                self._cr.commit()
            flag = flag + 1
        return True

    def action_create_purchase_order(self):
        po_obj = self.env['purchase.order']
        pol_obj = self.env['purchase.order.line']
        po_ids = []
        product_ids = []
        pol_recds = []
        po_val_dict = {}
        # if self.mapped('order_line.')
        for order in self:
            break
        res = po_obj.create({
                            'partner_id': order.instance_id.default_vendor_id.id,
                            'date_order': fields.datetime.now(),
                            # 'origin': order.name,
                            # 'so_id': order.id,
                        })

        for order in self:
            if order.order_line and (order.type == 'product' or order.order_line[0].product_id.type == 'product') and (order.qty_on_hand <= 0.0 or order.order_line[0].product_id.qty_on_hand <= 0.0):
                
                for data in order.order_line:
                    if data.product_id.id in product_ids:
                        pol_rec = pol_obj.search([('order_id', '=', res.id), ('product_id', '=', data.product_id.id)])
                        if pol_rec:
                            old_qty = pol_rec.product_qty
                            new_qty = old_qty + float(data.product_uom_qty)
                            pol_rec.product_qty = new_qty

                    else:
                        pricelist = order.instance_id.default_vendor_id.property_product_pricelist
                        partner_pricelist = order.instance_id.default_vendor_id.property_product_pricelist
                        if partner_pricelist:
                            product_context = dict(self.env.context, partner_id=order.instance_id.default_vendor_id.id, date=order.date_order, uom=data.product_uom.id)
                            final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id, data.product_uom_qty or 1.0, order.partner_id)
                        
                        else:
                            final_price = data.product_id.standard_price
                        val = {
                                'product_id': data.product_id.id,
                                'name': data.name,
                                'product_qty': data.product_uom_qty,
                                'product_uom': data.product_uom.id,
                                'date_planned': datetime.now(),
                                'price_unit': final_price,
                                'order_id': res.id,
                                }
                        pol_obj.create(val)
                        product_ids.append(data.product_id.id)
                    # if order.instance_id.default_vendor_id.id in po_val_dict.keys():
                    #     po_val_dict.get(order.instance_id.default_vendor_id.id).append(val)
                        
                    # else:
                    #     po_val_dict.update({
                    #         order.instance_id.default_vendor_id.id: [val]
                    #         })
                        
        # for key, vals in po_val_dict.items():
            
        #     for val in vals:
        #         pol_obj.create(val)
        if not res.order_line:
            res.button_cancel()
            res.unlink()
        if res:
            action = self.env.ref('purchase.purchase_rfq').read()[0]

            if len(res) > 1:
                action['domain'] = [('id', 'in', [res.id])]
            else:
                action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
                action['res_id'] = res and res.id

            return action

    @api.depends('po_ids')
    def _get_po_custom(self):
        
        for order in self:
            order.update({
                'po_count': len(set(self.po_ids.ids))
            })

    def action_view_po(self):
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        if len(self.po_ids) > 1:
            action['domain'] = [('id','in',self.po_ids.ids)]
        else:           
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = self.po_ids and self.po_ids[0].id 

        return action
    
    # @api.onchange('delivery_type')
    # def onchange_delivery_type(self):
    #     if self.delivery_type != 'dropship':
    #         raise Warning ('Currently Daraz is only support Dropship')

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
    
    def import_pending_orders_only(self, instance, job=False):
        if not job:
            job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})
        offset = 0
        res = self.connect_with_store('GetOrders', 'GET', instance_id=instance, extra_parameters={'Status':'pending'})
        result = res and res.get('SuccessResponse', {}).get('Body', {}).get('Orders', []) or {}
        total_count = res and res.get('SuccessResponse', {}).get('Head', {}).get('TotalCount', 0) or {}
        print("pending order",total_count)
        print("res", res)

        flag = 0
        if job:
            job.response = res
        for val in result:
            orderid = val.get('OrderId')
            if self.search([('instance_id', '=', instance.id), ('orderid', '=', orderid)]):
                continue
            status = val.get('Statuses', '')
            items_count = val.get('ItemsCount')
            res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})
            if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                time.sleep(60)
                res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance,  extra_parameters={'OrderId': orderid})
            if val:
                if flag > 10:
                    flag = 0
                    self._cr.commit()
                create_date = val.get('CreatedAt')
                update_date = val.get('UpdatedAt')
                first_name = val.get('CustomerFirstName', '')
                last_name = val.get('CustomerLastName', '')
                cust_name = "%s %s" % (first_name, last_name)
                order = self.create({
                        'partner_id': instance.default_customer_id.id,
                        'date_order': create_date,
                        'orderid': orderid,
                        'customer_name': cust_name,
                        'order_status': status and status[0],
                        'instance_id': instance.id,
                    })
                flag = flag + 1
                self.create_order_line(res and res.get('SuccessResponse', {}).get('Body', {}) or {}, items_count, order, instance)

        if result:
            # new_result += result
            offset = 100
            flag = 0
            while(total_count == 100):
                res = self.connect_with_store('GetOrders', 'GET', instance_id=instance, extra_parameters={'Offset': offset})
                print("sale order",res)
                child_result = res and res.get('SuccessResponse', {}).get('Body', {}).get('Orders', []) or {}
                total_count = res and res.get('SuccessResponse', {}).get('Head', {}).get('TotalCount', 0) or {}
                for val in child_result:
                    orderid = val.get('OrderId')
                    if self.search([('instance_id', '=', instance.id), ('orderid', '=', orderid)]):
                        continue
                    status = val.get('Statuses', '')
                    items_count = val.get('ItemsCount')
                    res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})
                    if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                        time.sleep(120)
                        res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance,  extra_parameters={'OrderId': orderid})
                    if val:
                        if flag > 10:
                            flag = 0
                            self._cr.commit()
                        create_date = val.get('CreatedAt')
                        update_date = val.get('UpdatedAt')
                        first_name = val.get('CustomerFirstName', '')
                        last_name = val.get('CustomerLastName', '')
                        cust_name = "%s %s" % (first_name, last_name)
                        order = self.create({
                            'partner_id': instance.default_customer_id.id,
                            'date_order': create_date,
                            'orderid': orderid,
                            'customer_name': cust_name,
                            'order_status': status and status[0],
                            'instance_id': instance.id,
                        })
                        flag = flag + 1
                        self.create_order_line(res and res.get('SuccessResponse', {}).get('Body', {}) or {}, items_count, order,
                                               instance)
                if child_result:
                    offset += 100

                else:
                    flag = 0
                    if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                        time.sleep(60)
                        res = self.connect_with_store('GetOrders', 'GET', instance_id=instance, extra_parameters={'Offset': offset})
                        after_result = res and res.get('SuccessResponse', {}).get('Body', {}).get('Orders', []) or {}
                        total_count = res and res.get('SuccessResponse', {}).get('Head', {}).get('TotalCount', 0) or {}
                        for val in after_result:
                            orderid = val.get('OrderId')
                            if self.search([('instance_id', '=', instance.id), ('orderid', '=', orderid)]):
                                continue
                            status = val.get('Statuses', '')
                            items_count = val.get('ItemsCount')
                            res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})
                            if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                                time.sleep(60)
                                res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})

                            if val:
                                # if flag > 10:
                                #     flag = 0

                                create_date = val.get('CreatedAt')
                                update_date = val.get('UpdatedAt')
                                first_name = val.get('CustomerFirstName', '')
                                last_name = val.get('CustomerLastName', '')
                                cust_name = "%s %s" % (first_name, last_name)
                                order = self.create({
                                    'partner_id': instance.default_customer_id.id,
                                    'date_order': create_date,
                                    'orderid': orderid,
                                    'customer_name': cust_name,
                                    'order_status': status and status[0],
                                    'instance_id': instance.id,
                                })
                                self.create_order_line(res and res.get('SuccessResponse', {}).get('Body', {})  or {}, items_count, order, instance)
                                self._cr.commit()
                    else:
                        break

        if result and job:
            job.env['process.job.line'].create({'job_id': job.id, 'message': "Empty Response"})

        return True

    def import_orders(self, instance, job=False):
        if not job:
            job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})
        offset = 0
        
        res = self.connect_with_store('GetOrders', 'GET', instance_id=instance, extra_parameters={'SortBy':'created_at', 'SortDirection': 'DESC'})
        result = res and res.get('SuccessResponse', {}).get('Body', {}).get('Orders', []) or {}
        total_count = res and res.get('SuccessResponse', {}).get('Head', {}).get('TotalCount', 0) or {}

        flag = 0
        if job:
            job.response = res
        for val in result:
            orderid = val.get('OrderId')
            if self.search([('instance_id', '=', instance.id), ('orderid', '=', orderid)]):
                continue
            status = val.get('Statuses', '')
            items_count = val.get('ItemsCount')
            res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})
            if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                time.sleep(60)
                res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance,  extra_parameters={'OrderId': orderid})
            if val:
                if flag > 10:
                    flag = 0
                    self._cr.commit()
                create_date = val.get('CreatedAt')
                update_date = val.get('UpdatedAt')
                first_name = val.get('CustomerFirstName', '')
                last_name = val.get('CustomerLastName', '')
                cust_name = "%s %s" % (first_name, last_name)
                order = self.create({
                        'partner_id': instance.default_customer_id.id,
                        'date_order': create_date,
                        'orderid': orderid,
                        'customer_name': cust_name,
                        'order_status': status and status[0],
                        'instance_id': instance.id,
                    })
                flag = flag + 1
                self.create_order_line(res and res.get('SuccessResponse', {}).get('Body', {})  or {}, items_count, order, instance)

        if result:
            # new_result += result
            offset = 100
            flag = 0
            while(total_count == 100):
                res = self.connect_with_store('GetOrders', 'GET', instance_id=instance, extra_parameters={'Offset': offset})
                child_result = res and res.get('SuccessResponse', {}).get('Body', {}).get('Orders', []) or {}
                total_count = res and res.get('SuccessResponse', {}).get('Head', {}).get('TotalCount', 0) or {}
                for val in child_result:
                    orderid = val.get('OrderId')
                    if self.search([('instance_id', '=', instance.id), ('orderid', '=', orderid)]):
                        continue
                    status = val.get('Statuses', '')
                    items_count = val.get('ItemsCount')
                    res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})
                    if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                        print()
                        time.sleep(120)
                        res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance,  extra_parameters={'OrderId': orderid})
                    if val:
                        if flag > 10:
                            flag = 0
                            self._cr.commit()
                        create_date = val.get('CreatedAt')
                        update_date = val.get('UpdatedAt')
                        first_name = val.get('CustomerFirstName', '')
                        last_name = val.get('CustomerLastName', '')
                        cust_name = "%s %s" % (first_name, last_name)
                        order = self.create({
                            'partner_id': instance.default_customer_id.id,
                            'date_order': create_date,
                            'orderid': orderid,
                            'customer_name': cust_name,
                            'order_status': status and status[0],
                            'instance_id': instance.id,
                        })
                        flag = flag + 1
                        self.create_order_line(res and res.get('SuccessResponse', {}).get('Body', {})  or {}, items_count, order,
                                               instance)
                if child_result:
                    offset += 100

                else:
                    flag = 0
                    if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                        time.sleep(60)
                        res = self.connect_with_store('GetOrders', 'GET', instance_id=instance, extra_parameters={'Offset': offset})
                        after_result = res and res.get('SuccessResponse', {}).get('Body', {}).get('Orders', []) or {}
                        total_count = res and res.get('SuccessResponse', {}).get('Head', {}).get('TotalCount', 0) or {}
                        for val in after_result:
                            orderid = val.get('OrderId')
                            if self.search([('instance_id', '=', instance.id), ('orderid', '=', orderid)]):
                                continue
                            status = val.get('Statuses', '')
                            items_count = val.get('ItemsCount')
                            res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})
                            if res and res.get('ErrorResponse', {}).get('Head', {}).get('ErrorCode', 0) == '429':
                                time.sleep(60)
                                res = self.connect_with_store('GetOrderItems', 'GET', instance_id=instance, extra_parameters={'OrderId': orderid})

                            if val:
                                # if flag > 10:
                                #     flag = 0

                                create_date = val.get('CreatedAt')
                                update_date = val.get('UpdatedAt')
                                first_name = val.get('CustomerFirstName', '')
                                last_name = val.get('CustomerLastName', '')
                                cust_name = "%s %s" % (first_name, last_name)
                                order = self.create({
                                    'partner_id': instance.default_customer_id.id,
                                    'date_order': create_date,
                                    'orderid': orderid,
                                    'customer_name': cust_name,
                                    'order_status': status and status[0],
                                    'instance_id': instance.id,
                                })
                                self.create_order_line(res and res.get('SuccessResponse', {}).get('Body', {})  or {}, items_count, order, instance)
                                self._cr.commit()
                    else:
                        break


        if result and job:
                job.env['process.job.line'].create({'job_id': job.id, 'message': "Empty Response"})

        return True

    @api.model
    def search_product(self, sku='', instance=False):
        product_obj = self.env['product.product']       
        product = product_obj.search(
            [('instance_id', '=', instance.id), ('default_code', '=', sku)], limit=1)
        if product:
            return product
        odoo_product = sku and product_obj.search([('default_code', '=', sku)], limit=1)
        if odoo_product:
            return odoo_product
        return False

    @api.model
    def create_product(self, name='', sku='', instance=False):
        product = self.env['product.product'].create({
            'name': name, 'default_code': sku, 'sku': sku, 'instance_id': instance.id,
            'type' : 'product',
        })
        return product

    @api.model
    def create_order_line(self, records ={}, qty=0.00, order=False, instance=False):
        for record in records.get('OrderItems', {}):
            item_id = record.get('OrderItemId')
            sku = record.get('Sku').replace(' ', '')
            name = record.get('Name', '')
            shop_sku = record.get('ShopSku')
            # res = self.connect_with_store('GetProducts', 'GET', instance_id=instance, extra_parameters={'search':sku})
            # result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
            # result.get('Products')
            
            product = self.search_product(sku, instance)
            if not product:
                product = self.create_product(name, sku, instance)
            price_unit = record.get('ItemPrice')

            line_extra_vals = {
                'item_id': item_id,
                'shop_id': record.get('ShopId'),
                'sku': sku,
                'shop_sku': shop_sku,
                'name': name,
                'shipping_type': record.get('ShippingType'),
                'price_unit': record.get('ItemPrice'),
                'paid_price': record.get('PaidPrice'),
                # 'currency': record.get('Currency'),
                'tax_amount': record.get('TaxAmount'),
                'shipping_amount': record.get('ShippingAmount'),
                'shipping_service_cost': record.get('ShippingServiceCost'),
                'voucher_amount': record.get('VoucherAmount'),
                'voucher_code': record.get('VoucherCode'),
                'daraz_status': record.get('Status'),
                'shipment_provider': record.get('ShipmentProvider'),
                'delivery': record.get('Delivery'),
                'is_digital': record.get('IsDigital'),
                'digital_delivery_info': record.get('DigitalDeliveryInfo'),
                'tracking_code': record.get('TrackingCode'),
                'tracking_code_pre': record.get('TrackingCodePre'),
                'reason': record.get('Reason'),
                'reason_detail': record.get('ReasonDetail'),
                'purchase_order_id': record.get('PurchaseOrderId'),
                'purchase_order_no': record.get('PurchaseOrderNumber'),
                'package_id': record.get('PackageId'),
                'promised_shipping_time': record.get('PromisedShippingTime'),
                'extra_attributes': record.get('ExtraAttributes'),
                'shipping_provider_type': record.get('ShippingProviderType'),
                'create_date': record.get('CreatedAt'),
                'update_date': record.get('UpdatedAt'),
                'return_status': record.get('ReturnStatus'),
                'product_main_image': record.get('productMainImage'),
                'variation': record.get('Variation'),
                'color_family': record.get('Color Family'),
                'product_detail_url': record.get('ProductDetailUrl'),
                'invoice_number': record.get('invoiceNumber')}

            line = self.create_sale_order_line(product, qty, name, order, price_unit)
            line.write(line_extra_vals)

    @api.model
    def create_sale_order_line(self, product, quantity,  name, order, price):

        sale_order_line_obj = self.env['sale.order.line']
        uom_id = product and product.uom_id and product.uom_id.id or False
        product_data = {
            'product_id': product and product.ids[0] or False,
            'order_id': order.id,
            'company_id': order.company_id.id,
            'product_uom': uom_id,
            'name': name,
            'display_type': False,
        }
        tmp_sale_line = sale_order_line_obj.new(product_data)
        tmp_sale_line.product_id_change()
        so_line_vals = sale_order_line_obj._convert_to_write(
            {name: tmp_sale_line[name] for name in tmp_sale_line._cache})
        
        so_line_vals.update(
            {
                'order_id': order.id,
                'product_uom_qty': quantity,
                'price_unit': price,
            }
        )
        line = sale_order_line_obj.create(so_line_vals)
        return line

    def update_orders(self):
        job_obj = self.env['process.job']
        # orders = self.env['sale.order'].search([('instance_id','=',instance.id),('update_order_status','=',True),('status_is_updated','=',False)])
        # for order in orders:
        line = self.order_line
        OrderItemIds = line.mapped('item_id')
        job = job_obj.create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})

        if self.order_status == 'pending':
            marketplace_res = self.connect_with_store('SetStatusToPackedByMarketplace', 'GET', instance_id=self.instance_id,
                extra_parameters={
                             'DeliveryType': 'dropship',
                             'OrderItemIds': json.dumps(OrderItemIds),
                             # 'ShippingProvider': self.shipping_provider,
                             # 'TrackingNumber' : line.tracking_no or '',
                             },job=job)
            marketplace_result = marketplace_res and marketplace_res.get('SuccessResponse', {}).get('Body', {}) or {}
            market_orderitems = marketplace_result.get('OrderItems',{})
            for market_orderitem in market_orderitems:
                if market_orderitem.get('OrderItemId'):
                    ShippingProvider = market_orderitem.get('ShipmentProvider','')
                    TrackingNumber = market_orderitem.get('TrackingNumber','')
                    line.tracking_no = TrackingNumber 
                    PackageId = market_orderitem.get('PackageId','')

            res = self.connect_with_store('SetStatusToReadyToShip', 'GET', instance_id=self.instance_id,
                extra_parameters={
                         'DeliveryType': 'dropship',
                         'OrderItemIds': json.dumps(OrderItemIds),
                         # 'ShippingProvider': ShippingProvider,
                         # 'TrackingNumber' : TrackingNumber,
                         
                         }, job=job)

            result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
            orderitems = result.get('OrderItems',{})
            for orderitem in orderitems:
                self.order_status = 'ready_to_ship'
                if orderitem.get('PurchaseOrderNumber'):
                    # line.purchase_order_id = orderitem.get('PurchaseOrderId','')
                    self.status_is_updated = True
                    line.purchase_order_no = orderitem.get('PurchaseOrderNumber','')

        # if not self.order_status == 'canceled':
            
        return
        
    @api.model
    def auto_import_sale_order(self, ctx={}):
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

            self.import_orders(instance, job)
            instance.so_import_next_execution = instance.so_import_cron_id.nextcall
        return True

    @api.model
    def auto_import_pending_order(self, ctx={}):
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

            self.import_pending_orders_only(instance, job)
            instance.pending_so_import_next_execution = instance.pending_so_import_cron_id.nextcall
        return True

    @api.model
    def auto_import_status_sale_order(self, ctx={}):
        flag = 0
        instance_obj = self.env["daraz.connector"]
        if not isinstance(ctx, dict) or not 'instance_id' in ctx:
            return True
        instance_id = ctx.get('instance_id', False)
        instance = instance_id and instance_obj.search(
            [('id', '=', instance_id), ('state', '=', 'connected')]) or False
        if instance:
            job = self.env['process.job'].create(
            {'instance_id': instance.id, 'process_type': 'order', 'operation_type': 'import',
             'message': 'Process for import Order status'})
            orders = self.env['sale.order'].search([('instance_id','=',instance.id)])
            for order in orders:               
                res = self.connect_with_store('GetOrder', 'GET', instance_id=instance, extra_parameters={'OrderId':order.orderid}, job=job)
                result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
                orderdata = result.get('Orders',[]) 
                status = orderdata and orderdata[0].get('Statuses','')
                if flag > 10:
                    flag = 0
                    self._cr.commit()
                if status:

                    flag = flag + 1
                    order.order_status = status and status[0]
            instance.so_import_next_execution = instance.so_import_cron_id.nextcall
        return True

    # @api.model
    # def auto_export_status_sale_order(self, ctx={}):
    #     instance_obj = self.env["daraz.connector"]
    #     if not isinstance(ctx, dict) or not 'instance_id' in ctx:
    #         return True
    #     instance_id = ctx.get('instance_id', False)
    #     instance = instance_id and instance_obj.search(
    #         [('id', '=', instance_id), ('state', '=', 'connected')]) or False
    #     if instance:
    #         job = self.env['process.job'].create(
    #         {'instance_id': instance.id, 'process_type': 'order', 'operation_type': 'export',
    #          'message': 'Process for export Order status'})
    #         self.update_orders(instance, job)
    #         instance.so_import_next_execution = instance.so_import_cron_id.nextcall
    #     return True

    def action_ready_to_ship(self):
        for order in self:
            order.update_orders()
        return True

    def daraz_order_cancel(self, flag=False):
        if not flag:
            action = self.env.ref('daraz_connector.action_wizard_prepare_cancel_reason').read()[0]
            action['views'] = [(self.env.ref('daraz_connector.view_cancel_reason_process_form').id, 'form')]
            action['res_id'] = self.env['cancel.reason'].create({'order_id': self.id}).id
            return action

        job_obj = self.env['process.job']
        for order in self:
            ReasonId = False
            if self.cancel_reason == 'delay':
                ReasonId = 10
            elif self.cancel_reason == 'out_of_stock':
                ReasonId = 15
            else:
                ReasonId = 21

            OrderItemIds = order.order_line.mapped('item_id')
            for OrderItemId in OrderItemIds:
                job = job_obj.create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Cancel Order status'})
                res = order.connect_with_store('SetStatusToCanceled', 'GET', instance_id=order.instance_id,
                    extra_parameters={
                             'OrderItemId': OrderItemIds and OrderItemIds[0],
                             'ReasonId': ReasonId
                             }, job=job)
                result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
                if result:
                    order.order_status = 'canceled'

        res = super(SaleOrder,self).action_cancel()

        return res


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    so_id = fields.Many2one('sale.order', string='Sale Order', copy=False)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    item_id = fields.Char('Order ItemId')
    shop_id = fields.Char('Shop Id')
    sku = fields.Char('Sku')
    shop_sku = fields.Char('Shop Sku')
    shipping_type = fields.Char('Shipping Type')
    paid_price = fields.Float('Paid Price')
    currency_id = fields.Many2one('res.currency', 'Currency')
    tax_amount = fields.Char('Tax Amount')
    shipping_amount = fields.Char('Shipping Amount')
    shipping_service_cost = fields.Char('Shipping Service Cost')
    voucher_amount = fields.Char('Voucher Amount')
    voucher_code = fields.Char('Voucher Code')
    daraz_status = fields.Char('Status')
    shipment_provider = fields.Char('Shipment Provider')
    delivery = fields.Char('Delivery')
    is_digital = fields.Char('Is Digital')
    digital_delivery_info = fields.Char('Digital Delivery Info')
    tracking_code = fields.Char('Tracking Code')
    tracking_code_pre = fields.Char('Tracking Code Pre')
    reason = fields.Char('Reason')
    reason_detail = fields.Char('Reason Detail')
    purchase_order_id = fields.Char('Purchase OrderId')
    purchase_order_no = fields.Char('Purchase Order Number')
    package_id = fields.Char('PackageId')
    promised_shipping_time = fields.Char('Promised Shipping Time')
    extra_attributes = fields.Char('Extra Attributes')
    shipping_provider_type = fields.Char('Shipping Provider Type')
    create_date = fields.Char('Created At')
    update_date = fields.Char('Updated At')
    return_status = fields.Char('Return Status')
    product_main_image = fields.Char('Product Main Image')
    variation = fields.Char('Variation')
    color_family = fields.Char('Color Family')
    product_detail_url = fields.Char('Product Detail Url')
    invoice_number = fields.Char('Invoice Number')
    tracking_no = fields.Char("Tracking No")
    serial_no = fields.Char("Serial No")

    # _sql_constraints = [
    #     ('code_sku_uniq', 'unique (code,sku)', 'The Sku of the account must be unique per company !')
    # ]
