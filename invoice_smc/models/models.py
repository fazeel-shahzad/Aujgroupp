# -*- coding: utf-8 -*-

from odoo import models, fields, api


class invone_smc(models.Model):
    _inherit = 'res.partner'

    no_cnic = fields.Char(string='CNIC')
    ntn = fields.Char(string='NTN')


class InheritField(models.Model):
    _inherit = 'account.move'

    freight = fields.Char(string='Details')
    journal_id = fields.Many2one("account.journal",string='Journal id')


