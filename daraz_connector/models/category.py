# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import Warning
from datetime import datetime ,timezone
import requests
import urllib.parse
from hashlib import sha256
from hmac import HMAC
import json


class darazCategory(models.Model):
    _inherit = "product.category"

    leaf = fields.Boolean("Leaf",default=False)
    darazCategoryId = fields.Integer("Daraz CategoGetCategoryAttributesry ID")
    darazStoreId = fields.One2many('daraz.connector', 'id', string="Daraz Store")

    def doConnection(self, action=None, req=None, instance=False):
        url = instance.api_url
        key = instance.api_key
        action = action if action else "GetCategoryTree"
        format = "json"
        userId = instance.userId
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
        parameters['Signature'] = HMAC(key.encode('utf-8'), data,
                                       sha256).hexdigest()
        headers = {'Content-Type': "application/json",'Accept': "*/*", 'Connection': "keep-alive",'cache-control': "no-cache" }
        try:
            response = requests.request(method, url, headers=headers, params=parameters)
        except Exception as e:
            raise Warning(_(response.text))
        return json.loads(response.text)

    def createCategory(self, record, parent=None, instance=False):
        category_obj  = self.env['product.category']
        name = record.get("name")
        categoryId = record.get("categoryId")
        attribute_obj = self.env["product.attribute"]
        attribute_obj.import_attribute(instance, categoryId)
        leaf = record.get("leaf")
        if parent is not None:
            category = category_obj.create({"name": name, "darazCategoryId": categoryId, "leaf": leaf,"parent_id":parent })
        else:
            category = category_obj.create({"name": name,"darazCategoryId": categoryId, "leaf": leaf })
        return category.id

    def import_category(self, instance):
        res = self.doConnection('GetCategoryTree','GET', instance)
        result = self.rec(res.get('SuccessResponse').get('Body'), parent=None, instance=instance)
        
        return
        
    def rec(self, data, parent=None, instance=False):
        for record in data:
            if record.get('leaf') == False:
                parent_id = self.createCategory(record, parent, instance)

                self.rec(record.get('children'), parent_id, instance)
            else:
                self.createCategory(record, parent=None, instance=instance)
        return True


