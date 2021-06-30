from odoo import models, fields, api, _
from odoo.exceptions import Warning,ValidationError


class SaleOrderCommission(models.Model):
    _name = 'sale.order.commission'
    _rec_name = 'salesperson'
    _order = "id desc"

    commission_structure_id = fields.Many2one('commission.structure.ecotech', 'Commission Structure')
    salesperson = fields.Many2one('res.users',string="Salesperson")
    net_amount = fields.Float(string="Net Amount")
    net_commission = fields.Float(string="Net Commission")
    sale_order_ids = fields.Many2many('sale.order', string="Sales Orders")
    general_amount = fields.Float(string='General Amount')
    deduct_amount = fields.Char(string='Deduction Amount')
    general_cal = fields.Char('Commission Calculated')
    general_commission = fields.Float(string='General Commission')
    special_amount = fields.Float(string='Special Amount')
    special_commission = fields.Float(string='Special Commission')
    special_commission_line_ids = fields.One2many('special.commission.line', 'sales_commission_id', 'Special Commission Calculation')
    state = fields.Selection([
        ('draft','Draft'),
        ('locked','Locked')
    ],'State',default='draft')

    def action_lock_commission(self):
        for rec in self:
            if rec.state == 'draft':
                rec.write({'state':'locked'})

    def action_reset_commission(self):
        if len(self) > 1:
            for user in self.mapped('salesperson'):
                last = self.search([('salesperson','=',user.id)],order='create_date desc')[0]
                last.write({'state':'draft'})
        else:
            other_draft = self.search([('state','=','draft'),('salesperson','=',self.salesperson.id)])
            if other_draft:
                raise Warning('Please lock other draft state commission record of this particular User.')
            else:
                self.write({'state':'draft'})

    def unlink(self):
        for rec in self:
            [order.write({'is_commission_created':False}) for order in rec.sale_order_ids]
        return super(SaleOrderCommission, self).unlink()


    def action_view_sales(self):
        action = self.env.ref('sale.action_orders').read()[0]

        sale_orders = self.sale_order_ids
        if len(sale_orders) > 1:
            action['domain'] = [('id', 'in', sale_orders.ids)]
        elif sale_orders:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = sale_orders.id
        return action


class SpecialCommissionLine(models.Model):
    _name = 'special.commission.line'

    sales_commission_id = fields.Many2one('sale.order.commission')
    product_id = fields.Many2one('product.product', 'Product')
    qty_sold = fields.Integer('Drums')
    amount = fields.Float('Total Amount')
    cal = fields.Char('Commission Calculated Per Drum')
    commission = fields.Float('Commission Amount')