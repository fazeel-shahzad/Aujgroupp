# Part of AktivSoftware
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrderLine(models.Model):
    """Inherited Sale Order Line to add fields.

    :param Do not update: To skill update pricelist from SO Confirm.
    """

    _inherit = 'product.pricelist'

    is_to_be_skipped = fields.Boolean(string='Do not update')
