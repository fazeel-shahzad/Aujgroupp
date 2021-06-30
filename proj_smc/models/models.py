# -*- coding: utf-8 -*-

from odoo import models, fields, api





class inherit_proj_smc(models.Model):
    _inherit = 'purchase.order'


    reference = fields.Char("Reference No.",compute="name_gets")
    start_shipping_date = fields.Datetime("Start Shipping Date")
    arrival_date = fields.Datetime("Arrival Date")
    status_changing_manually = fields.Selection([('arrive_at_lahore', 'Arrived At Lahore'), ('arrive_at_karachi', 'Arrived At Karachi')],
                                      string="Status Changing Manually")


    def name_gets(self):


        for rec in self:
            rec.reference = 'SMC-'+rec.name





