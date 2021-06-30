from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date


class SalesCommissionWizard(models.TransientModel):
    _name = 'sales.commission.wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    user_ids = fields.Many2many('res.users', string="Sales Persons")
    ignore_late_payments = fields.Boolean('Ignore Sales with late payments')
    late_payments_exceed = fields.Integer('Late payments exceeds to')

    @api.constrains('date_from', 'date_to')
    def dates_constrains(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError('Date To Must Be Greater Than Date From.')

    def ignore_unpaid_orders(self, sales_orders):
        eligible_sale_orders = self.env['sale.order']
        for order in sales_orders:
            paid_invoices = order.invoice_ids.filtered(lambda x:x.invoice_payment_state == 'paid' and x.type == 'out_invoice')
            if paid_invoices:
                paid_amount = sum(paid_invoices.mapped('amount_total'))
                needs_to_pay = order.amount_total
                if paid_amount >= needs_to_pay:
                    last_paid_invoice_date = max(paid_invoices.mapped('invoice_date'))
                    if last_paid_invoice_date and last_paid_invoice_date >= self.date_from and last_paid_invoice_date <= self.date_to:
                        if self.ignore_late_payments:
                            payment_due_days = (last_paid_invoice_date - order.date_order.date()).days
                            if payment_due_days >= self.late_payments_exceed:
                                continue
                        eligible_sale_orders += order
        return eligible_sale_orders

    def action_generate_commissions(self):
        if not self.user_ids:
            self.user_ids = self.env['res.users'].search([])
        user_id_list = self.user_ids and self.user_ids.ids or []

        sales_orders = self.env['sale.order'].search([('is_commission_created', '=', False),('user_id', 'in', user_id_list)])
        sale_orders = self.ignore_unpaid_orders(sales_orders)
        user_wise_so = {}
        for user in sale_orders.mapped('user_id'):
            so_of_this_user = sale_orders.filtered(lambda x:x.user_id == user)
            user_wise_so.update({user:so_of_this_user})

        commission_obj = self.env['sale.order.commission']
        special_comm_line = self.env['special.commission.line']
        for user,sale_orders in user_wise_so.items():
            re_calculate_sales = False
            existing = self.env['sale.order.commission'].search([('salesperson', '=', user.id),('state','=','draft')],
                                                                limit=1)
            if existing and sale_orders:
                re_calculate_sales = existing.mapped('sale_order_ids')
                existing.unlink()
            sale_orders = sale_orders + re_calculate_sales if re_calculate_sales else sale_orders

            vals = {}
            structure_id = user.commission_structure_id
            if not structure_id:
                continue

            order_lines = sale_orders.mapped('order_line')
            exclude_products = structure_id.exclude_line_ids.mapped('product_id')

            special_lines = order_lines.filtered(lambda x:x.product_id in exclude_products)
            special_sales = sum(special_lines.mapped('price_subtotal'))
            general_lines = order_lines.filtered(lambda x:x.product_id not in exclude_products)
            general_sales = sum(general_lines.mapped('price_subtotal'))
            net_sales = general_sales + special_sales
            if structure_id.deduction_type:
                if structure_id.deduction_type == 'fixed':
                    deduct_sales = general_sales - structure_id.deduction_amount
                    deduct_amount = str(structure_id.deduction_amount) + '/-'
                else:
                    deduct_sales = (general_sales * structure_id.deduction_amount) / 100
                    deduct_amount = str(structure_id.deduction_amount) + '%'
            else:
                deduct_sales = (net_sales)

            sale_ids = [(6, 0, sale_orders.ids)]
            vals.update({
                'commission_structure_id':structure_id.id,
                'salesperson':user.id,
                'general_amount':general_sales,
                'special_amount':special_sales,
                'net_amount':net_sales,
                'sale_order_ids':sale_ids,
                'deduct_amount':deduct_amount
            })

            for line in structure_id.commission_line_ids:
                if general_sales >= line.amount_above and general_sales < line.amount_less_than:
                    general_cal = str(line.commission_percent) + '%'
                    general_commission = (deduct_sales * line.commission_percent) / 100
                    vals.update({
                        'general_cal':general_cal,
                        'general_commission':general_commission
                    })

            commission_id = commission_obj.create(vals)

            for line in structure_id.exclude_line_ids:
                order_line = special_lines.filtered(lambda x : x.product_id == line.product_id)
                total_price = sum(order_line.mapped('price_subtotal'))
                total_qty = sum(order_line.mapped('product_uom_qty'))
                if line.compute_type == 'percentage':
                    cal = str(line.commission_per_drum) + '%'
                    commission = (total_price * line.commission_per_drum) / 100
                else:
                    cal = str(line.commission_per_drum) + '/-'
                    commission = total_qty * line.commission_per_drum
                special_vals = {
                    'sales_commission_id':commission_id.id,
                    'product_id':line.product_id.id,
                    'qty_sold':total_qty,
                    'amount':total_price,
                    'cal':cal,
                    'commission':commission
                }
                special_comm_line.create(special_vals)

            special_commission = sum(commission_id.mapped('special_commission_line_ids').mapped('commission'))
            net_commission = commission_id.general_commission + special_commission
            commission_id.write({
                'special_commission':special_commission,
                'net_commission':net_commission
            })
            [order.write({'is_commission_created':True}) for order in sale_orders]
        return {'effect': {'fadeout': 'slow',
                           'message': "Yeah %s, It's Done." % self.env.user.name,
                           'img_url': '/web/static/src/img/smile.svg', 'type': 'rainbow_man'}}
