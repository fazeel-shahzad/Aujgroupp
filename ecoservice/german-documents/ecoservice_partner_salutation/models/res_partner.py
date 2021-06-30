# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import fields, models


class ResPartnerTitle(models.Model):
    _inherit = 'res.partner.title'

    salutation = fields.Char(
        translate=True,
    )
