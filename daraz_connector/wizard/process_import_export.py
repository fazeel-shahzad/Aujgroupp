from odoo import models, fields, api
from odoo.exceptions import Warning
from _collections import OrderedDict


class ImportExportProcess(models.TransientModel):
    _name = 'import.export.process'
    _description = "Import Export Process"

    is_import_order = fields.Boolean("Order Import ?", default=False, help="Import Remaining Orders.")
    import_order_status = fields.Boolean("Import & Update Order status to odoo", default=False, help="Export Order Status to daraz.")
    is_import_category = fields.Boolean("Category Import ?", default=False, help="Import Categories.")
    is_import_attribute = fields.Boolean("Attribute Import ?", default=False, help="Import Attributes.")
    is_import_product = fields.Boolean("Product Import ?", default=False, help="Import Products.")
    is_import_transaction = fields.Boolean("Transaction Import ?", default=False, help="Import Transaction.")
    is_import_pending_orders = fields.Boolean("Pending Order Import ?", default=False, help="Import Remaining Orders.")
    is_import_docs = fields.Boolean("Document Import ?", default=False, help="Import Documents.")
    instance_ids = fields.Many2many("daraz.connector", string="Stores")

    @api.onchange('is_import_order')
    def alllocation(self):
        location_ids = self.env['daraz.connector'].sudo().search([])
        self.instance_ids = location_ids

    @api.model
    def default_get(self, fields):
        res = super(ImportExportProcess, self).default_get(fields)
        if 'default_instance_id' in self._context:
            res.update({'instance_ids': [(6, 0, [self._context.get('default_instance_id')])]})
        elif 'instance_ids' in fields:
            instances = self.env['daraz.connector'].search([('state', '=', 'confirm')])
            res.update({'instance_ids': [(6, 0, instances.ids)]})
        return res

    def import_sale_orders(self):
        so_obj = self.env['sale.order']
        for instance in self.instance_ids:
            so_obj.import_orders(instance)
        return True

    def import_pending_orders(self):
        so_obj = self.env['sale.order']
        for instance in self.instance_ids:
            so_obj.import_pending_orders_only(instance)
        return True

    def action_import_docs(self):
        so_obj = self.env['sale.order']
        for instance in self.instance_ids:
            so_obj.import_docs(instance)
        return True

    def action_import_transactions(self):
        transc_obj = self.env['transaction.detail']
        for instance in self.instance_ids:
            transc_obj.import_transactions(instance)
            self._cr.commit()
        return True

    def import_sale_orders_status(self):
        so_obj = self.env['sale.order']

        for instance in self.instance_ids:
            so_obj.import_order_status(instance)
        return True

    def import_categories(self):
        category_obj = self.env["product.category"]
        for instance in self.instance_ids:
            category_obj.import_category(instance)

        return True

    def import_attribute(self):
        attribute_obj = self.env["product.attribute"]
        for instance in self.instance_ids:
            attribute_obj.import_attributes(instance)

        return True

    def import_product(self):
        product_obj = self.env["product.product"]
        for instance in self.instance_ids:
            product_obj.import_product(instance)

        return True
