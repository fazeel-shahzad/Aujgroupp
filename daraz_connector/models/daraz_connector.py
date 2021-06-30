from odoo import models, fields, api,_
from odoo.exceptions import Warning
from datetime import datetime ,timezone
import requests
from dateutil.relativedelta import relativedelta
import urllib.parse
from hashlib import sha256
from hmac import HMAC

_intervalTypes = {
    'work_days': lambda interval: relativedelta(days=interval),
    'days': lambda interval: relativedelta(days=interval),
    'hours': lambda interval: relativedelta(hours=interval),
    'weeks': lambda interval: relativedelta(days=7 * interval),
    'months': lambda interval: relativedelta(months=interval),
    'minutes': lambda interval: relativedelta(minutes=interval),
}


class DarazConnector(models.Model):
    _name = "daraz.connector"
    _description = "Daraz Connector"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char("Store Name", index=True, required=True)
    api_url = fields.Char("Api Url", required=True)
    userId = fields.Char("User ID", required=True)
    api_key = fields.Char("Api Key", required=True)
    default_customer_id = fields.Many2one('res.partner', string='Default Daraz Customer')
    default_vendor_id = fields.Many2one('res.partner', string='Default Purchase Vendor')
    state = fields.Selection([("draft", 'Draft'), ("connected", 'Connected')], default='draft')
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self: self.env.user.company_id.id)
    fees_account_id = fields.Many2one('account.account', string='Fees Account')
    import_pending_orders = fields.Boolean(string='Import Only Pending Orders?')
    pending_so_import_cron_id = fields.Many2one('ir.cron')
    pending_so_import_interval_number = fields.Integer('Import Pending Order Interval Number', help="Repeat every x.", default=10)
    pending_so_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Pending Order Interval Unit')
    pending_so_import_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    pending_so_import_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)

    so_auto_import = fields.Boolean('Auto Import Sale Order?')
    so_import_cron_id = fields.Many2one('ir.cron')
    so_import_interval_number = fields.Integer('Import Sale Order Interval Number', help="Repeat every x.", default=10)
    so_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Sale Order Interval Unit')
    so_import_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    so_import_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)

    trans_auto_import = fields.Boolean('Auto Import Transaction?')
    trans_import_cron_id = fields.Many2one('ir.cron')
    trans_import_interval_number = fields.Integer('Import Transaction Interval Number', help="Repeat every x.", default=10)
    trans_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Transaction Interval Unit')
    trans_import_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    trans_import_user_id = fields.Many2one('res.users', string="User", help='Cron User', default=lambda self: self.env.user)

    trans_set_so = fields.Boolean('Auto Set So in Transaction?')
    trans_set_so_cron_id = fields.Many2one('ir.cron')
    trans_set_so_interval_number = fields.Integer('Set SO Transaction Interval Number', help="Repeat every x.", default=10)
    trans_set_so_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Transaction Interval Unit')
    trans_set_so_next_execution = fields.Datetime('Next Execution', help='Set So Next execution time')
    trans_set_so_user_id = fields.Many2one('res.users', string="User", help='Set So Transaction Cron User', default=lambda self: self.env.user)

    trans_create_invoice = fields.Boolean('Auto Create Invoice from Transaction?')
    trans_create_invoice_cron_id = fields.Many2one('ir.cron')
    trans_create_invoice_interval_number = fields.Integer('inv Transaction Interval Number', help="Repeat every x.", default=10)
    trans_create_invoice_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'invoice Transaction Interval Unit')
    trans_create_invoice_next_execution = fields.Datetime('invoice create Next Execution', help='Next execution time')
    trans_create_invoice_user_id = fields.Many2one('res.users', string="User", help='invoice create  Cron User', default=lambda self: self.env.user)


    so_auto_import_status = fields.Boolean('Auto Import Status Sale Order?')
    so_import_status_cron_id = fields.Many2one('ir.cron')
    so_import_status_interval_number = fields.Integer('Import Status Sale Order Interval Number', help="Repeat every x.", default=10)
    so_import_status_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Status Sale Order Interval Unit')
    so_import_status_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    so_import_status_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)
    
    so_auto_update = fields.Boolean("Auto Update Sale Order?",
                                    help="Will automatically update order details to the Daraz.")
    so_update_cron_id = fields.Many2one('ir.cron')
    so_update_interval_number = fields.Integer('Update Sale Order Interval Number', help="Repeat every x.", default=10)
    so_update_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Update Sale Order Interval Unit')
    so_update_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    so_update_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)

    prod_auto_import = fields.Boolean('Auto Import Product?')
    prod_import_cron_id = fields.Many2one('ir.cron')
    prod_import_interval_number = fields.Integer('Import Product Interval Number', help="Repeat every x.", default=10)
    prod_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Product Interval Unit')
    prod_import_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    prod_import_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)

    attribute_auto_import = fields.Boolean('Auto Import Attribute?')
    attribute_import_cron_id = fields.Many2one('ir.cron')
    attribute_import_interval_number = fields.Integer('Import Attribute Interval Number', help="Repeat every x.", default=10)
    attribute_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Attribute Interval Unit')
    attribute_import_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    attribute_import_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)

    categ_auto_import = fields.Boolean('Auto Import Category?')
    categ_import_cron_id = fields.Many2one('ir.cron')
    categ_import_interval_number = fields.Integer('Import Category Interval Number', help="Repeat every x.", default=10)
    categ_import_interval_type = fields.Selection([('minutes', 'Minutes'),
                                                ('hours', 'Hours'), ('work_days', 'Work Days'), ('days', 'Days'),
                                                ('weeks', 'Weeks'), ('months', 'Months')],
                                               'Import Category Interval Unit')
    categ_import_next_execution = fields.Datetime('Next Execution', help='Next execution time')
    categ_import_user_id = fields.Many2one('res.users', string="User", help='User', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        res = super(DarazConnector, self).create(vals)
        if 'so_auto_import' in vals:
            res.setup_import_so_cron()
        if 'so_auto_update' in vals:
            res.setup_update_so_cron()
        if 'so_auto_import_status' in vals:
            res.setup_import_status_so_cron()

        if 'trans_auto_import' in vals:
            res.setup_import_trans_cron()
        if 'trans_set_so' in vals:
            res.setup_so_in_trnsd_cron()
        if 'trans_create_invoice' in vals:
            res.setup_crea_inv_trnsd_cron()

        if 'pro_auto_import' in vals:
            res.setup_import_prod_cron()
        if 'categ_auto_import' in vals:
            res.setup_import_categ_cron()
        if 'attribute_auto_import' in vals:
            res.setup_update_so_cron()
       
        return res

    def write(self, vals):
        res = super(DarazConnector, self).write(vals)
        for instance in self:
            if 'so_auto_import' in vals:
                instance.setup_import_so_cron()
            if 'so_auto_update' in vals:
                instance.setup_update_so_cron()

            if 'trans_auto_import' in vals:
                instance.setup_import_trans_cron()
            if 'trans_set_so' in vals:
                instance.setup_so_in_trnsd_cron()
            if 'trans_create_invoice' in vals:
                instance.setup_crea_inv_trnsd_cron()

            if 'pro_auto_import' in vals:
                instance.setup_import_prod_cron()
            if 'categ_auto_import' in vals:
                instance.setup_import_categ_cron()
            if 'attribute_auto_import' in vals:
                instance.setup_update_so_cron()
            if 'so_auto_import_status' in vals:
                instance.setup_import_status_so_cron()
            
        return res

    def setup_import_trans_cron(self):
        if self.trans_auto_import:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_transaction_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.trans_import_interval_type](self.trans_import_interval_number)
            vals = {
                'active': True,
                'interval_number': self.trans_import_interval_number,
                'interval_type': self.trans_import_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_transaction(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.trans_import_user_id and self.trans_import_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    import_trans_cron = self.env.ref('daraz_connector.ir_cron_import_status_orders')
                except:
                    import_trans_cron = False
                if not import_trans_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + import_trans_cron.name
                vals.update({'name': name})
                new_cron = import_trans_cron.copy(default=vals)
                import_trans_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_import_transaction_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                import_trans_cron and self.update({'trans_import_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_transaction_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_so_in_trnsd_cron(self):
        if self.trans_set_so:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_transaction_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.trans_set_so_interval_type](self.trans_set_so_interval_number)
            vals = {
                'active': True,
                'interval_number': self.trans_set_so_interval_number,
                'interval_type': self.trans_set_so_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_set_so_transaction(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.trans_set_so_user_id and self.trans_set_so_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    set_so_trans_cron = self.env.ref('daraz_connector.ir_cron_set_so_transaction')
                except:
                    set_so_trans_cron = False
                if not set_so_trans_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + set_so_trans_cron.name
                vals.update({'name': name})
                new_cron = set_so_trans_cron.copy(default=vals)
                set_so_trans_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_set_so_transaction_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                set_so_trans_cron and self.update({'trans_set_so_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_set_so_transaction_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_crea_inv_trnsd_cron(self):
        if self.trans_create_invoice:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_cre_inv_transaction_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.trans_create_invoice_interval_type](self.trans_create_invoice_interval_number)
            vals = {
                'active': True,
                'interval_number': self.trans_create_invoice_interval_number,
                'interval_type': self.trans_create_invoice_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_cre_inv_transaction(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.trans_create_invoice_user_id and self.trans_create_invoice_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    crt_inv_trans_cron = self.env.ref('daraz_connector.ir_cron_cre_inv_transaction')
                except:
                    crt_inv_trans_cron = False
                if not crt_inv_trans_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + crt_inv_trans_cron.name
                vals.update({'name': name})
                new_cron = crt_inv_trans_cron.copy(default=vals)
                crt_inv_trans_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_cre_inv_transaction_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                crt_inv_trans_cron and self.update({'trans_create_invoice_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_cre_inv_transaction_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_import_so_cron(self):
        if self.so_auto_import:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.so_import_interval_type](self.so_import_interval_number)
            vals = {
                'active': True,
                'interval_number': self.so_import_interval_number,
                'interval_type': self.so_import_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_sale_order(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.so_import_user_id and self.so_import_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    import_so_cron = self.env.ref('daraz_connector.ir_cron_import_orders')
                except:
                    import_so_cron = False
                if not import_so_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + import_so_cron.name
                vals.update({'name': name})
                new_cron = import_so_cron.copy(default=vals)
                import_so_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_import_orders_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                import_so_cron and self.update({'so_import_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_import_status_so_cron(self):
        if self.so_auto_import_status:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_status_orders_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.so_import_status_interval_type](self.so_import_status_interval_number)
            vals = {
                'active': True,
                'interval_number': self.so_import_status_interval_number,
                'interval_type': self.so_import_status_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_status_sale_order(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.so_import_status_user_id and self.so_import_status_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    import_status_so_cron = self.env.ref('daraz_connector.ir_cron_import_status_orders')
                except:
                    import_status_so_cron = False
                if not import_status_so_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + import_status_so_cron.name
                vals.update({'name': name})
                new_cron = import_status_so_cron.copy(default=vals)
                import_status_so_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_import_status_orders_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                import_status_so_cron and self.update({'so_import_status_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_status_orders_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_import_categ_cron(self):
        if self.categ_auto_import:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.categ_import_interval_type](self.categ_import_interval_number)
            vals = {
                'active': True,
                'interval_number': self.categ_import_interval_number,
                'interval_type': self.categ_import_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_sale_order(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.categ_import_user_id and self.categ_import_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    import_categ_cron = self.env.ref('daraz_connector.ir_cron_import_orders')
                except:
                    import_categ_cron = False
                if not import_categ_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + import_categ_cron.name
                vals.update({'name': name})
                new_cron = import_categ_cron.copy(default=vals)
                import_categ_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_import_orders_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                import_categ_cron and self.update({'categ_import_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_import_prod_cron(self):
        if self.prod_auto_import:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.prod_import_interval_type](self.prod_import_interval_number)
            vals = {
                'active': True,
                'interval_number': self.prod_import_interval_number,
                'interval_type': self.prod_import_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_sale_order(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.prod_import_user_id and self.prod_import_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    import_prod_cron = self.env.ref('daraz_connector.ir_cron_import_orders')
                except:
                    import_prod_cron = False
                if not import_prod_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + import_prod_cron.name
                vals.update({'name': name})
                new_cron = import_prod_cron.copy(default=vals)
                import_prod_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_import_orders_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                import_prod_cron and self.update({'prod_import_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_import_attribute_cron(self):
        if self.attribute_auto_import:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.attribute_import_interval_type](self.attribute_import_interval_number)
            vals = {
                'active': True,
                'interval_number': self.attribute_import_interval_number,
                'interval_type': self.attribute_import_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_import_sale_order(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.attribute_import_user_id and self.attribute_import_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    import_attribute_cron = self.env.ref('daraz_connector.ir_cron_import_orders')
                except:
                    import_attribute_cron = False
                if not import_attribute_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + import_attribute_cron.name
                vals.update({'name': name})
                new_cron = import_attribute_cron.copy(default=vals)
                import_attribute_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_import_orders_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                import_attribute_cron and self.update({'attribute_import_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_import_orders_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True

    def setup_update_so_cron(self):
        if self.so_auto_update:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_update_orders_%d' % (self.id),
                                              raise_if_not_found=False)
            except:
                cron_available = False
            nextcall = datetime.now()
            nextcall += _intervalTypes[self.so_update_interval_type](self.so_update_interval_number)
            vals = {
                'active': True,
                'interval_number': self.so_update_interval_number,
                'interval_type': self.so_update_interval_type,
                'nextcall': nextcall.strftime('%Y-%m-%d %H:%M:%S'),
                'code': "model.auto_update_order_status(ctx={'instance_id':%d})" % (self.id),
                'user_id': self.so_update_user_id and self.so_update_user_id.id}

            if cron_available:
                vals.update({'name': cron_available.name})
                cron_available.write(vals)
            else:
                try:
                    update_so_cron = self.env.ref('daraz_connector.ir_cron_update_orders')
                except:
                    update_so_cron = False
                if not update_so_cron:
                    raise Warning(
                        'Please upgrade Daraz Connector module.')

                name = self.name + ' : ' + update_so_cron.name
                vals.update({'name': name})
                new_cron = update_so_cron.copy(default=vals)
                update_so_cron = self.env['ir.model.data'].create({'module': 'daraz_connector',
                                                                   'name': 'ir_cron_update_orders_%d' % (self.id),
                                                                   'model': 'ir.cron',
                                                                   'res_id': new_cron.id,
                                                                   'noupdate': True
                                                                   })
                update_so_cron and self.update({'so_update_cron_id': new_cron.id})
        else:
            try:
                cron_available = self.env.ref('daraz_connector.ir_cron_update_orders_%d' % (self.id))
            except:
                cron_available = False

            if cron_available:
                cron_available.write({'active': False})
        return True
    
    def button_reset(self):
        self.write({'state': 'draft'})
        return True

    def doConnection(self, action=None, req=None):
        url = self.api_url
        key = self.api_key
        action = action if action else "GetBrands"
        format = "json"
        userId = self.userId
        method = req if req else 'GET'
        self.state = 'connected'
        super(DarazConnector, self).write({"state":"connected"})
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

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "*/*",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        try:
            response = requests.request(method, url, headers=headers, params=parameters)
            print(response)

        except Exception as e:
            raise Warning(_(response.text))

        if response.status_code == 200:
            self.state = 'connected'
            self.env.cr.commit()
            raise Warning(
                _("Successfully Connected"))

        return response.text