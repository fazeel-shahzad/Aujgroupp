from odoo import models, fields, api, _



class CommissionStructure(models.Model):
    _name = 'commission.structure.ecotech'

    def _get_default_deduction_amount(self):
        for rec in self:
            if rec.deduction_type == 'fixed':
                return 0.0
            else:
                return 1.0

    name = fields.Char(string="Name")
    deduction_amount = fields.Float(string="Deduction Amount",default=_get_default_deduction_amount)
    deduction_type = fields.Selection([('fixed', 'Fixed Amount'), ('percentage', 'Percentage')],
                                      'Deduction Type To Compute', default='fixed')
    commission_line_ids = fields.One2many('commission.structure.line', 'commission_id',
                                         string="Commission Structure Ranges")
    exclude_line_ids = fields.One2many('exclude.structure.line', 'commission_id', string="Exclude From Computation")

    def action_view_users(self):
        action = self.env.ref('base.action_res_users').read()[0]

        users = self.env['res.users'].search([('commission_structure_id', '=', self.id),
                                              ('commission_structure_id','!=',False)])
        if not users:
            return {'effect':{'fadeout':'slow',
                              'message':"Ohh %s, None of the Users associated with this Commission Structure." %
                                        self.env.user.name,
                              'img_url':'/web/static/src/img/warning.png', 'type':'rainbow_man'}}

        if len(users) > 1:
            action['domain'] = [('id', 'in', users.ids)]
        elif users:
            action['views'] = [(self.env.ref('base.view_users_form').id, 'form')]
            action['res_id'] = users.id
        return action


class CommissionStructureLine(models.Model):
    _name = 'commission.structure.line'

    commission_id = fields.Many2one("commission.structure.ecotech")
    amount_above = fields.Float(string="Price Total More or Equal")
    amount_less_than = fields.Float(string="Price Total Less Than")
    commission_percent = fields.Float(string="Commission Percentage (%)")



class CommissionExcludeLine(models.Model):
    _name= 'exclude.structure.line'

    commission_id = fields.Many2one("commission.structure.ecotech")
    product_id = fields.Many2one('product.product', 'Product To Be Excluded')
    commission_per_drum = fields.Float(string='Commission Per Drum')
    compute_type = fields.Selection([('fixed', 'Per Drum'), ('percentage', 'Percentage')],
                                      'Type To Compute',default='fixed')