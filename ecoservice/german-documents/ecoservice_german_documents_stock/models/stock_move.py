# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import models


# We need this for the mixin
class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'eco_report.mixin']
