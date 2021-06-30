# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from functools import partial

from odoo import api, fields, models, _
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total', 'order_line.discount_type',
                 'order_line.discount', 'global_order_discount', 'global_discount_type')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            total_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                if line.discount_type == 'fixed':
                    total_discount += line.discount
                else:
                    total_discount += line.product_uom_qty * (line.price_unit - line.price_reduce)

            IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
            discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
            if not discTax:
                discTax = 'untax'
            total_global_discount = 0.0

            if discTax == 'taxed':
                total = amount_untaxed + amount_tax
            else:
                total = amount_untaxed

            if order.global_discount_type == 'fixed':
                total_global_discount = order.global_order_discount
            else:
                total_global_discount = total * (order.global_order_discount or 0.0) / 100
            total -= total_global_discount
            total_discount += total_global_discount

            if discTax != 'taxed':
                total = total + amount_tax

            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': total,
                'total_global_discount': total_global_discount,
                'total_discount': total_discount,
            })

    def _amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                if line.discount_type == 'fixed' and line.product_uom_qty:
                    price_reduce = line.price_unit - (line.discount / line.product_uom_qty)
                else:
                    price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
                taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
                for tax in line.tax_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]

    total_global_discount = fields.Monetary(string='Total Global Discount', store=True,
                                            readonly=True, compute='_amount_all')
    total_discount = fields.Monetary(string='Discount', store=True, readonly=True,
                                     compute='_amount_all', tracking=True)
    global_discount_type = fields.Selection(
        [('fixed', 'Fixed'), ('percent', 'Percent')], string="Discount Type", default="percent",
        help="If global discount type 'Fixed' has been applied then no partial invoice will be generated for this order.")
    global_order_discount = fields.Float(string='Global Discount', store=True, tracking=True)

    def _create_invoices(self, grouped=False, final=False):
        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)
        moves._compute_amount()
        return moves

    def _prepare_invoice(self):
        invoiceVals = super(SaleOrder, self)._prepare_invoice()
        if self.global_order_discount:
            if self.global_discount_type == 'fixed':
                lines = self.order_line.filtered(
                    lambda l: not l.is_downpayment and l.product_uom_qty != l.qty_to_invoice)
                # if lines:
                #     raise UserError(_("This action is going to make partial invoice for the less quantity delivered of this order. It will not be allowed because 'Fixed' type global discount has been applied."))
            invoiceVals.update({
                'global_discount_type': self.global_discount_type,
                'global_order_discount': self.global_order_discount
            })
        return invoiceVals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(string='Discount', digits='Discount', default=0.0)
    discount_type = fields.Selection([('fixed', 'Fixed'),
                                      ('percent', 'Percent')],
                                     string="Discount Type",
                                     default="percent")

    @api.depends('product_uom_qty', 'discount_type', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            quantity = 1.0
            if line.discount_type == 'fixed':
                price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                quantity = line.product_uom_qty
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, quantity,
                                            product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        discount = self.discount
        if self.discount_type == 'fixed' and self.product_uom_qty:
            discount = (discount * self.qty_to_invoice) / self.product_uom_qty
        res.update({
            'discount_type': self.discount_type,
            'discount': discount,
        })
        return res

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        if not (self.product_id and self.product_uom and
                self.order_id.partner_id and self.order_id.pricelist_id and
                self.order_id.pricelist_id.discount_policy == 'without_discount' and
                self.env.user.has_group('product.group_discount_per_so_line')):
            return

        self.discount = 0.0
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id,
            fiscal_position=self.env.context.get('fiscal_position')
        )

        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)

        if new_list_price != 0:
            if self.order_id.pricelist_id.currency_id != currency:
                # we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
                new_list_price = currency._convert(
                    new_list_price, self.order_id.pricelist_id.currency_id,
                    self.order_id.company_id or self.env.company, self.order_id.date_order or fields.Date.today())
            rule = self.order_id.pricelist_id.with_context(
                product_context)._get_pricelist_item([
                    (self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
                ])
            if rule and rule.compute_price == 'fixed':
                discount = (new_list_price - price) * (self.product_uom_qty or 1.0)
                discount_type = 'fixed'
            else:
                discount = (new_list_price - price) / new_list_price * 100
                discount_type = 'percent'
            if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
                self.discount = discount
                self.discount_type = discount_type


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_pricelist_item(self, products_qty_partner, date=False, uom_id=False):
        if not date:
            date = self._context.get('date') or fields.Date.today()
        date = fields.Date.to_date(date)  # boundary conditions differ if we have a datetime
        if not uom_id and self._context.get('uom'):
            uom_id = self._context['uom']
        if uom_id:
            # rebrowse with uom if given
            products = [item[0].with_context(uom=uom_id) for item in products_qty_partner]
            products_qty_partner = [
                (products[index], data_struct[1], data_struct[2])
                for index, data_struct in enumerate(products_qty_partner)
            ]
        else:
            products = [item[0] for item in products_qty_partner]

        if not products:
            return {}

        categ_ids = {}
        for p in products:
            categ = p.categ_id
            while categ:
                categ_ids[categ.id] = True
                categ = categ.parent_id
        categ_ids = list(categ_ids)

        is_product_template = products[0]._name == "product.template"
        if is_product_template:
            prod_tmpl_ids = [tmpl.id for tmpl in products]
            # all variants of all products
            prod_ids = [
                p.id for p in list(
                    chain.from_iterable(
                        [t.product_variant_ids for t in products]))
            ]
        else:
            prod_ids = [product.id for product in products]
            prod_tmpl_ids = [product.product_tmpl_id.id for product in products]

        items = self._compute_price_rule_get_items(products_qty_partner, date,
                                                   uom_id, prod_tmpl_ids, prod_ids, categ_ids)
        return items[0] if items else False
