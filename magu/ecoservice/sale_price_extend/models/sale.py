# Part of AktivSoftware
# See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    """Inherited to manage pricelist on confirm.

    :param Updated sale price: To store price i.e. calculated form pricelist.
    :param Apply changes boolean: To mark to update price on pricelist.
    """

    _inherit = 'sale.order.line'

    so_line_price = fields.Float(string='Updated sale price')
    apply_changed_price = fields.Boolean(
        string='Apply Price Change on Pricelist', copy=False)

    @api.onchange('product_id', 'product_uom', 'product_uom_qty')
    def set_so_line_price(self):
        """Pricelist Amount.

        To set base amount before change.
        :return: None, Set amount in extra field of line.
        """
        self.so_line_price = self.price_unit


class SaleOrder(models.Model):
    """Inherited SO.

    To manage unit price list on SO line.
    """

    _inherit = 'sale.order'

    @api.onchange('sale_order_template_id')  # noqa: C901
    def onchange_sale_order_template_id(self):
        """Add updated sale price in template.

        When quotation has template then it must also have price difference.
        :return: None
        """
        if not self.sale_order_template_id:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return
        template = self.sale_order_template_id.with_context(
            lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        so_line = self.env['sale.order.line']
        context_date = fields.Date.context_today(self)
        for line in template.sale_order_template_line_ids:
            data = self._compute_line_data_for_template_change(line)
            if line.product_id:
                discount = 0
                if self.pricelist_id:
                    price = self.pricelist_id.with_context(
                        uom=line.product_uom_id.id).get_product_price(
                        line.product_id, 1, False)
                    if self.pricelist_id.discount_policy == \
                            'without_discount' and line.price_unit:
                        discount = (line.price_unit - price
                                    ) / line.price_unit * 100
                        # negative discounts (= surcharge) are included in the
                        # display price
                        if discount < 0:
                            discount = 0
                        else:
                            price = line.price_unit
                    elif line.price_unit:
                        price = line.price_unit
                else:
                    price = line.price_unit

                data.update({
                    'price_unit': price,
                    'discount': 100 - ((100 - discount) * (
                            100 - line.discount) / 100),
                    'product_uom_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'customer_lead': self._get_customer_lead(
                        line.product_id.product_tmpl_id),
                    'so_line_price': price,
                })
                if self.pricelist_id:
                    data.update(so_line._get_purchase_price(
                        self.pricelist_id,
                        line.product_id,
                        line.product_uom_id,
                        context_date))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = [(5, 0, 0)]
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))
        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = context_date + timedelta(
                template.number_of_days)

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note

    def action_confirm(self):
        """On confirm SO.

        If unit price not change in order line then wizard are not open.
        If the customer clicks on YES while creating a new price,
        the new price should be stored in a customer specific list
        (list has the name of the customer) and
        should not be changed in the original list.
        If the customer does not yet have his own specific list,
        it should be created.
        :return: Wizard to update new price in pricelist
        """
        # Check if the Confirm is Pressed from Wizard
        if self.env.context.get('from_wizard'):
            return super(SaleOrder, self).action_confirm()
        filtered_so_lines = self.order_line.filtered(
            lambda line: line.price_unit != line.so_line_price)

        # If Any Mismatch in Product Price Found
        if not filtered_so_lines:
            return super(SaleOrder, self).action_confirm()

        # Set the Order Line Ids in Context for the Wizard
        ctx = self.env.context.copy() or {}
        ctx.update({
            'so_line_list': filtered_so_lines.ids,
        })
        return {
            'name': 'Update new price in pricelist.',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order.line.product.price.wizard',
            'views': [(False, 'form')],
            'target': 'new',
            'context': ctx,
        }
