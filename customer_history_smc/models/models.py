

from odoo import models, fields, api,_




class vendor_invoice(models.Model):
    _name = 'vendor.invoices'


    name = fields.Char(string="Invoice No")
    branch = fields.Char("Branch")
    branch_code = fields.Char(string="Branch Code")
    partner_id = fields.Char(string="ID")
    architect = fields.Char(string="Architect")
    sale_consultant = fields.Char(string="Sales Consultant ")
    sale_consultant_code = fields.Char(string="Sale Consultant Code")
    customer_name = fields.Many2one("res.partner",string="Customer Name")
    customer_code = fields.Char(string="Customer Code")

    order_date = fields.Date(string="Order Date")
    invoice_amount = fields.Float(string="Invoice Amount")
    transaction_date = fields.Date(string="Transaction Date")
    pending_amount = fields.Float(string="Pending Amount")
    product_name = fields.Char(string="Product Name")
    article = fields.Char(string="Article")
    finish = fields.Char(string="Finish")
    quantity = fields.Char(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    discount = fields.Float(string="Discount")
    tax = fields.Float(string="Tax")
    uom = fields.Char(string="UOM")
    sub_total = fields.Char(string="Sub Total")




class ContactInherit(models.Model):
    _inherit = 'res.partner'





    def SmartButton(self):
        print(self.self)

        return {
            'name': _('Customer History'),
            'domain': [('customer_name', '=', self.self.id)],

            'view_mode': 'tree',
            'res_model': 'vendor.invoices',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',

        }
