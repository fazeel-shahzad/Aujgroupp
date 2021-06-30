# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class SaleReport(models.Model):
    _inherit = "sale.report"

    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
        ], string="Discount Type", readonly=True)
    discount = fields.Float('Discount fixed or %', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['discount_type'] = ", l.discount_type as discount_type"
        groupby += ', l.discount_type'

        query = super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
        query = query.replace(
            "sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) as discount_amount",
            "CASE WHEN l.discount_type = 'fixed' THEN sum((l.discount / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) ELSE sum((l.price_unit * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) END as discount_amount"
        )
        return query
