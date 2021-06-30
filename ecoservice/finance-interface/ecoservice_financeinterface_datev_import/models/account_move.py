# -*- coding: utf-8 -*-
# Part of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    import_datev = fields.Many2one(comodel_name='import.datev', string='DATEV Import', readonly=True)
