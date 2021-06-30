# Part of AktivSoftware
# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductPriceWizard(models.TransientModel):
    """Update Customer Priclist Price Wizard.

    To manage price of customer pricelist if its changed on SO Lines.
    """

    _name = 'sale.order.line.product.price.wizard'
    _description = 'SO Line Product Price Change Selection Wizard'

    def _default_get_so_products(self):
        """SO Lines.

        Lines ids will pass from SO Confirm in context.
        :return: SO Lines Record Set.
        """
        return self.env['sale.order.line'].browse(
            self.env.context.get('so_line_list'))

    so_product_ids = fields.Many2many(
        'sale.order.line', default=_default_get_so_products)

    #     so_product_ids = fields.Many2many('sale.order.line')

    @api.model
    def action_confirm(self, so):
        """Confirm SO.

        To confirm SO with with from wizard flag.
        :param so: Sale Order.
        :return: None.
        """
        so.with_context({'from_wizard': True}).action_confirm()

    def action_confirm_on_cancel(self):
        """Cancel Button.

        It will simply call SO Confirm and do not update any pricelist.
        :return: None.
        """
        self.action_confirm(self.so_product_ids.mapped('order_id'))

    def update_lines(self, products, pl_items, checked_lines):
        """Update Pricelist Lines.

        :param products: Ids of Products.
        :param pl_items: Pricelist Lines.
        :param checked_lines: Lines with new price.
        :return: None
        """
        for prd_id in products:
            pl_items.filtered(lambda l: l.product_id.id == prd_id).write({
                'fixed_price': checked_lines.filtered(
                    lambda l: l.product_id.id == prd_id
                ).price_unit
            })

    def change_customer_pricelist_product_price(self):
        """Yes Button.

        Pricelist will be updated based on:
        Do Not Update Boolean in pricelist (TO make pricelist as public)
        If user click on 'Yes' then,
        - We will Fetch the selected product list from the Wizard  and  will
        check below criteria and update price in
        customer pricelist accordingly:

        1. We will check if customer-specific price list is available or not,
            if there is no pricelist is available for customer
            then we will create new one with updated price.

        2. If Customer-Specific price list available
        then we will check for the product entry,
        If an product entry is added then we will update the price
        else we will create new entry of product in
        customer specific price list with updated price.

        Note: We will not update price on Product
        :return: None.
        """

        checked_lines = self.so_product_ids.filtered(
            lambda ln: ln.apply_changed_price)
        if not checked_lines:
            raise UserError(_(
                'Please select product to update.\n'
                'If you do not want to change price then please Cancel.'
            ))
        so_id = checked_lines.mapped('order_id')
        pricelist = so_id.partner_id.property_product_pricelist

        if pricelist.is_to_be_skipped:
            pricelist = pricelist.search([
                ('name', '=', so_id.partner_id.name)
            ])
            if not pricelist:
                pricelist = pricelist.create({
                    'name': so_id.partner_id.name
                })
            so_id.partner_id.property_product_pricelist = pricelist.id

        so_prd_ids = checked_lines.product_id
        pl_items = pricelist.item_ids
        pl_prd_ids = pl_items.product_id

        common = list(set(pl_prd_ids.ids).intersection(set(so_prd_ids.ids)))
        different = list(set(so_prd_ids.ids).difference(set(pl_prd_ids.ids)))
        if common == different:
            self.update_lines(list(common), pl_items, checked_lines)
        else:
            pricelist_item = self.env['product.pricelist.item']
            exist_product = checked_lines.filtered(
                lambda line: line.product_id.id in pl_items.product_id.ids
            )
            if exist_product:
                self.update_lines(
                    exist_product.product_id.ids, pl_items, exist_product)
            new_lines = checked_lines.filtered(
                lambda line: line.id not in exist_product.ids
            )
            if new_lines:
                vals = []
                for line in new_lines:
                    vals.append({
                        'applied_on': '0_product_variant',
                        'min_quantity': 0,
                        'product_tmpl_id': line.product_id.product_tmpl_id.id,
                        'product_id': line.product_id.id,
                        'compute_price': 'fixed',
                        'fixed_price': line.price_unit,
                        'pricelist_id': pricelist.id,
                    })
                pricelist_item.create(vals)
        self.action_confirm(so_id)
