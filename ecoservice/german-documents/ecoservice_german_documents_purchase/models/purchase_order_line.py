# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import models


# We need this for the mixin
class PurchaseOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = ['purchase.order.line', 'eco_report.mixin']
