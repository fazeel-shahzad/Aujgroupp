# -*- coding: utf-8 -*-
from odoo import api, models


class StockReportCustom(models.AbstractModel):
    _name = 'report.stock_report_pdf.report_stock_document'

    def get_sales(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        records = self.env['stock.picking'].search(
            [('scheduled_date', '>', rec_model.date_from), ('state', '=', 'done'),
             ('scheduled_date', '<', rec_model.date_to), ('picking_type_id', '=', picking_incoming.id)])
        total_qty = 0
        for rec in records:
            if rec.origin:
                if rec.origin.split()[0] != 'Return':
                    for line in rec.move_ids_without_package:
                        if line.product_id.id == product.id:
                            total_qty = total_qty + line.quantity_done
        return total_qty

    def get_sale_return(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        records = self.env['stock.picking'].search(
            [('scheduled_date', '>', rec_model.date_from),('state', '=', 'done'),
             ('scheduled_date', '<', rec_model.date_to), ('picking_type_id', '=', picking_incoming.id)])
        total_qty = 0
        for rec in records:
            if rec.origin:
                if rec.origin.split()[0] == 'Return':
                    for line in rec.move_ids_without_package:
                        if line.product_id.id == product.id:
                            total_qty = total_qty + line.quantity_done
        return total_qty

    def get_purchase(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        records = self.env['stock.picking'].search(
            [('scheduled_date', '>', rec_model.date_from), ('state', '=', 'done'),
             ('scheduled_date', '<', rec_model.date_to), ('picking_type_id', '=', picking_incoming.id)])
        total_qty = 0
        for rec in records:
            if rec.origin:
                if rec.origin.split()[0] != 'Return':
                    for line in rec.move_ids_without_package:
                        if line.product_id.id == product.id:
                            total_qty = total_qty + line.quantity_done
        return total_qty

    def get_purchase_return(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        records = self.env['stock.picking'].search(
            [('scheduled_date', '>', rec_model.date_from), ('state', '=', 'done'),
             ('scheduled_date', '<', rec_model.date_to), ('picking_type_id', '=', picking_incoming.id)])
        total_qty = 0
        for rec in records:
            if rec.origin:
                if rec.origin.split()[0] == 'Return':
                    for line in rec.move_ids_without_package:
                        if line.product_id.id == product.id:
                            total_qty = total_qty + line.quantity_done
        return total_qty

    def get_opening_balance(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        picking_out = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        records_out = self.env['stock.picking'].search(
            [('state', '=', 'done'),('scheduled_date', '<', rec_model.date_from), ('picking_type_id', '=', picking_out.id)])

        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        records_in = self.env['stock.picking'].search(
            [('state', '=', 'done'), ('scheduled_date', '<', rec_model.date_from), ('picking_type_id', '=', picking_incoming.id)])
        total_qty_out = 0
        for rec in records_out:
            if rec.origin:
                # if rec.origin.split()[0] != 'Return':
                for line in rec.move_ids_without_package:
                    if line.product_id.id == product.id:
                        total_qty_out = total_qty_out + line.quantity_done
        total_qty_in = 0
        for rec in records_in:
            if rec.origin:
                # if rec.origin.split()[0] != 'Return':
                for line in rec.move_ids_without_package:
                    if line.product_id.id == product.id:
                        total_qty_in = total_qty_in + line.quantity_done
        total = total_qty_in - total_qty_out
        return total

    def get_last_price(self, product):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        # records = self.env['account.move'].search([('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
        records = self.env['purchase.order'].search([('date_approve', '>', rec_model.date_from),
                                ('date_approve', '<', rec_model.date_to), ('state', '=', 'purchase')])
        price = 0
        for rec in records:
            for line in rec.order_line:
                if line.product_id.id == product.id:
                    if line.price_unit > 0:
                        price = line.price_unit
                        break
        return price

    def get_inventory_adjustment_purchase(self, product):
        location = self.env['stock.location'].search([('name', '=', 'Stock'), ('location_id.name', '=', 'MWS')])
        location_2 = self.env['stock.location'].search([('name', '=', 'E-BIKE: Production'),
                                                      ('location_id.name', '=', 'Virtual Locations')])
        print(location)
        total_qty = 0

        # if location_2:
        #     records = self.env['stock.move.line'].search([('product_id', '=', product.id),
        #                                                   ('location_dest_id', '=', location_2[0].id)])
        #     if records:
        #         for rec in records:
        #             if rec.reference == 'Product Quantity Updated':
        #                 total_qty = total_qty + rec.qty_done

        if location:
            records = self.env['stock.move.line'].search([('product_id', '=', product.id), ('location_dest_id', '=', location.id)])
            if records:
                for rec in records:
                    if rec.reference == 'INV:Inventory adjustment 24-12-2020':
                        total_qty = total_qty + rec.qty_done
        return total_qty

    def get_inventory_adjustment_sale(self, product):
        location = self.env['stock.location'].search([('name', '=', 'E-BIKE: Production'),
                                                      ('location_id.name', '=', 'Virtual Locations')])
        location_2 = self.env['stock.location'].search([('name', '=', 'E-BIKE: Inventory adjustment'),
                                                       ('location_id.name', '=', 'Virtual Locations')])
        total_qty = 0
        if location:
            records = self.env['stock.move.line'].search([('product_id', '=', product.id),
                                                          ('location_dest_id', '=', location.id)])
            if records:
                for rec in records:
                    if rec.reference != 'Product Quantity Updated':
                        total_qty = total_qty + rec.qty_done
        if location_2:
            records = self.env['stock.move.line'].search([('product_id', '=', product.id),
                                                          ('location_dest_id', '=', location_2.id)])
            if records:
                for rec in records:
                    # if rec.reference == 'Product Quantity Updated' or rec.reference == 'INV:Inventory':
                    total_qty = total_qty + rec.qty_done
        return total_qty

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        currencies = self.env['res.currency'].search([('name', '=', 'PKR')], limit=1)
        return {
            'doc_ids': self.ids,
            'doc_model': 'stock_report_pdf.stock.report.wizard',
            'purchase': self.get_purchase,
            'purchase_return': self.get_purchase_return,
            'sale_return': self.get_sale_return,
            'sale': self.get_sales,
            'last_price': self.get_last_price,
            'inventory_adjustment_purchase': self.get_inventory_adjustment_purchase,
            'inventory_adjustment_sale': self.get_inventory_adjustment_sale,
            'opening_balance': self.get_opening_balance,
            'products': rec_model.product_ids,
            'date_from': rec_model.date_from.date(),
            'date_to': rec_model.date_to.date(),
            'currency': currencies,
        }
