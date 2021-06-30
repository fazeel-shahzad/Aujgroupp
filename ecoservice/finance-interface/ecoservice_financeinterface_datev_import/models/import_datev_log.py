# -*- coding: utf-8 -*-
# Part of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class ImportDatevLog(models.Model):
    _name = 'import.datev.log'
    _order = 'id desc'

    name = fields.Text(string='Name')
    parent_id = fields.Many2one(comodel_name='import.datev', string='Import', ondelete='cascade')
    date = fields.Datetime(string='Time', readonly=True, default=lambda *a: fields.Datetime.today())
    state = fields.Selection(
        selection=[
            ('info', 'Info'),
            ('error', 'Error'),
            ('standard', 'Ok')
        ],
        string='State', select=True, readonly=True, default='info'
    )
