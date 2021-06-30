from odoo import models, fields, api


class ProcessJob(models.Model):
    _name = 'process.job'
    _order = 'id desc'
    _description = "Process Job"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name = fields.Char('Name', default=lambda self: self.env['ir.sequence'].next_by_code('process.job'))
    instance_id = fields.Many2one('daraz.connector', "Daraz Store")
    line_ids = fields.One2many('process.job.line', 'job_id', "Process Job Line")
    request = fields.Char("Request")
    response = fields.Text("Response")
    process_type = fields.Selection(
        [('product', 'Product'), ('order', 'Order'), ('customer', 'Customer'),
         ('category', 'Product Category'),('transaction','Transaction'), ('attribute', 'Product Attribute'), 
         ('attribute_val', 'Product Attribute Value'),('payment_gateway', 'Payment Gateway')], "Process Type")
    operation_type = fields.Selection(
        [('import', 'Import'), ('import_sync', 'Import/Sync'), ('export', 'Export'), ('update', 'Update')],
        "Operation Type")
    message = fields.Text("Message")


class ProcessJobLine(models.Model):
    _name = 'process.job.line'
    _order = 'id desc'
    _description = "Process Job"

    job_id = fields.Many2one("process.job", "Process Job")
    message = fields.Char("Message")
