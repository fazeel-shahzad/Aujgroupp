# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, timezone

import base64
from odoo import models, fields
from odoo import modules
class ProductProduct(models.Model):
    _inherit = 'product.product'

    parent_sku = fields.Char(string='Parent SKU')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    store_name1 = fields.Char(string='Testing')
    store_name = fields.Char(string='Store Name')
    multi_sku = fields.Many2many('multi.sku', string='Child SKUs')
    parent_sku = fields.Char(string='Parent SKU')
    entrepreneur = fields.Char(string='Entrepreneur')
    sub_account = fields.Char(string='Sub Account')

   

   


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_brand = fields.Many2one("product.brand", string="Market")
    sku_related = fields.Char(string='Parent SKU')




class SaleOrder(models.Model):
    _inherit = 'sale.order'




    product_brand = fields.Many2one("product.brand", string="Market")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    sku_related = fields.Char(string='SKU')
    parent_sku = fields.Char(string='Parent SKU')
    entrepreneur = fields.Char(string='Entrepreneur')
    sub_account = fields.Char(string='Sub Account')
    attachment = fields.Many2many('ir.attachment', String="Video Attachment")
    shipped_status = fields.Selection([('not shipped', 'Not Shipped'), ('shipped', 'Shipped'),('ask', 'Product not Received'), ('not_deliverd', 'Product not delivered'),('returned', 'Physically Returned'),('damage', 'Received Damaged Product ask for Claim'), ('claimed', 'Claimed'),  ('received', 'Claimed Received')], 'Shipped Status', readonly=True, default='not shipped')
   



class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char(string='Market Name')
    sku_name = fields.Char(string='Parent SKU')

class DarazConnector(models.Model):
    _inherit = 'daraz.connector'

    entrepreneur = fields.Char(string='Entrepreneur')
    sub_account = fields.Char(string='Sub Account')


class MultiSKU(models.Model):
    _name = 'multi.sku'
    _description = 'Multi.SKU'

    sku_name = fields.Char(string=' SKU')


class Return(models.TransientModel):
    _inherit = 'stock.return.picking'

    qc_name = fields.Char(string='Return Reason',required=True)
    store_name = fields.Char(string='Store Name',required=True)
    enterpreneur = fields.Char(string='Enterpreneur',required=True)
    subaccount = fields.Char(string='Sub Account')
    order_name = fields.Char(string='Order No',required=True)
    received_date = fields.Datetime(string='Return Received date',required=True)
    reason = fields.Text(string='What kind of Damage')
    order_state = fields.Selection([('yes', 'Yes'),('no', 'No')], string='Quality Check',required=True)
    product_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Damage ?',required=True)








