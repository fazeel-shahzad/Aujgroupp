# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import Warning
from datetime import datetime ,timezone
import requests
import urllib.parse
from hashlib import sha256
from hmac import HMAC
import json


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_dz_product = fields.Boolean("Is Daraz Product?")
    instance_id = fields.Many2one('daraz.connector', 'Daraz Store')
    sku = fields.Char('Sku')
    export_to_daraz = fields.Boolean("Export To Daraz?")


    def doConnection(self, action=None, req=None, instance_id=False):
        darazStore = instance_id
        url = darazStore.api_url
        key = darazStore.api_key
        action = action if action else "GetProducts"
        format = "json"
        userId = darazStore.userId
        method= req if req  else 'GET'

        now = datetime.now().timestamp()
        test = datetime.fromtimestamp(now, tz=timezone.utc).replace(microsecond=0).isoformat()
        parameters = {
            'UserID': userId,
            'Version': "1.0",
            'Action':action,
            'Format': format,
            'Timestamp': test}
        concatenated = urllib.parse.urlencode(sorted(parameters.items()))
        data = concatenated.encode('utf-8')
        parameters['Signature'] = HMAC(key.encode('utf-8'), data,sha256).hexdigest()
        headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        try:
            response = requests.request(method, url, headers=headers, params=parameters)
        except Exception as e:
            raise Warning(_(response.text))
        return json.loads(response.text)

    def import_product(self, instance):
        res = self.doConnection('GetProducts','GET', instance)
        result = res.get('SuccessResponse', {}).get('Body', {})

        if result:
            product = self.create_product(result, instance)

        return  

    def create_product(self, records, parent=None):
        product_obj = self.env['product.product']
        name = records.get("name")
        product = product_obj.create({
                "name": name, 
                
                })
        return

    # def create_expo_product(self, records, parent=None):
    #     # res = self.doConnection('CreateProduct','GET', instance)
    #     # result = res.get('SuccessResponse', {}).get('Body', {})
    #     #
    #     # if result:
    #     #     product = self.create_product(result, instance)
    #
    #     return


    def doConnection(self, action=None, req=None, instance_id=False):
        darazStore = instance_id
        url = darazStore.api_url
        key = darazStore.api_key
        action = action if action else "CreateProduct"
        format = "json"
        userId = darazStore.userId
        method= req if req  else 'GET'

        now = datetime.now().timestamp()
        test = datetime.fromtimestamp(now, tz=timezone.utc).replace(microsecond=0).isoformat()
        parameters = {
            'UserID': userId,
            'Version': "1.0",
            'Action':action,
            'Format': format,
            'Timestamp': test}
        concatenated = urllib.parse.urlencode(sorted(parameters.items()))
        data = concatenated.encode('utf-8')
        parameters['Signature'] = HMAC(key.encode('utf-8'), data,sha256).hexdigest()
        headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        try:
            response = requests.request(method, url, headers=headers, params=parameters)
        except Exception as e:
            raise Warning(_(response.text))
        return json.loads(response.text)

    def import_category_tree(self, instance=False, job=False):
        self.ensure_one()
        if not instance:
            instance = self.instance_id
        if not job:
            job = self.env['process.job'].create({'instance_id': self.instance_id.id, 'process_type': 'order', 'operation_type': 'export', 'message': 'Process for export Order status'})
        
        res = self.connect_with_store('GetCategoryTree', 'GET', instance_id=instance)
        result = res and res.get('SuccessResponse', {}).get('Body', {}) or {}
        if job:
            job.response = res
        if result:
            categid = result.get('CategoryId')
            name = val.get('Name')
            child = val.get('Children',{})
            print(categid,name,child)
            # attachment = self.env['ir.attachment'].create({
            #                                    'name': file_name,
            #                                    'datas': file,
            #                                    'res_model': 'sale.order', 
            #                                    'res_id' : self.id,
            #                                   # 'type': 'binary'
            #                                  })

            
        else:
            if job:
                job.env['process.job.line'].create({'job_id': job.id, 'message': "Empty Response"})

        return True


    def export_to_daraz(self):

        res = """<?xml version="1.0" encoding="UTF-8" ?>
                <Request>
                    <Product>
                        <PrimaryCategory>6614</PrimaryCategory>
                        <SPUId></SPUId>
                        <Attributes>
                            <name>api create product test sample</name>
                            <short_description>This is a nice product</short_description>
                            <brand>Remark</brand>
                            <model>asdf</model>
                            <kid_years>Kids (6-10yrs)</kid_years>
                        </Attributes>
                        <Skus>
                            <Sku>
                                <SellerSku>api-create-test-1</SellerSku>
                                <color_family>Green</color_family>
                                <size>40</size>
                                <quantity>1</quantity>
                                <price>388.50</price>
                                <package_length>11</package_length>
                                <package_height>22</package_height>
                                <package_weight>33</package_weight>
                                <package_width>44</package_width>
                                <package_content>this is whats in the box</package_content>
                                <Images>
                                    <Image>http://sg.s.alibaba.lzd.co/original/59046bec4d53e74f8ad38d19399205e6.jpg</Image>
                                    <Image>http://sg.s.alibaba.lzd.co/original/179715d3de39a1918b19eec3279dd482.jpg</Image>
                                </Images>
                            </Sku>
                            <Sku>
                                <SellerSku>api-create-test-2</SellerSku>
                                <color_family>Green</color_family>
                                <size>41</size>
                                <quantity>2</quantity>
                                <price>520.88</price>
                                <package_length>11</package_length>
                                <package_height>22</package_height>
                                <package_weight>33</package_weight>
                                <package_width>44</package_width>
                                <package_content>this is whats in the box</package_content>
                                <Images>
                                    <Image>http://sg.s.alibaba.lzd.co/original/59046bec4d53e74f8ad38d19399205e6.jpg</Image>
                                    <Image>http://sg.s.alibaba.lzd.co/original/179715d3de39a1918b19eec3279dd482.jpg</Image>
                                </Images>
                            </Sku>
                        </Skus>
                    </Product>
                </Request>"""

        return 

