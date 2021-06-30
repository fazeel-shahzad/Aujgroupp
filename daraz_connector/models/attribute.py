# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import Warning
from datetime import datetime ,timezone
import requests
import urllib.parse
from hashlib import sha256
from hmac import HMAC
import json


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    instance_id = fields.Many2one('daraz.connector', 'Daraz Store')
    attribute_type = fields.Char("Attribute Type")
    input_type = fields.Text(string="Input Type")
    is_mandatory = fields.Boolean(string="Is Mandatory?")
    is_sale_prop = fields.Boolean(string="Is Sale Prop?")
    label  = fields.Char(string="Label")

    def doConnection(self, action=None, req=None, instance_id=False, categoryId=''):
        darazStore = instance_id
        url = darazStore.api_url
        key = darazStore.api_key
        action = action if action else "GetCategoryAttributes"
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
            'PrimaryCategory' : categoryId,
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

    def import_attributes(self, instance, categoryId=False):
        res = self.doConnection('GetCategoryAttributes','GET', instance, categoryId)
        result = res.get('SuccessResponse', {}).get('Body', {})

        if result:
            attribute = self.create_attribute(result, instance)

        return  
        
    def import_attribute(self, instance, categoryId=False):
        res = self.doConnection('GetCategoryAttributes','GET', instance, categoryId)
        result = res.get('SuccessResponse', {}).get('Body', {})

        if result:
            attribute = self.create_attribute(result, instance)

        return  

    def create_attribute(self, records, parent=None):
        attribute_obj = self.env['product.attribute']
        for record in records:

            name = record.get("name")
            attribute = attribute_obj.create({
                    "name": name, 
                    "attribute_type " : record.get("Attribute Type",''),
                    "input_type " : record.get("Input Type",''),
                    "is_mandatory " : record.get("Is Mandatory?",False),
                    "is_sale_prop " : record.get("Is Sale Prop?",False),
                    "label " : record.get("Label"),
                    })
        return