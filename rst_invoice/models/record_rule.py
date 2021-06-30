from odoo import models, fields, api


class IRRuleForInvoice(models.Model):
    _inherit = 'ir.rule'

    def fix_er_role(self):
        rol_id = self.env.ref('account.account_move_see_all')
        # rol_id = self.env['ir.rule'].search([('id', '=', rol_id)])
        # rol_id.write({'domain_force': ['|', '|', ('company_id', '=', user.company_id.id), ('company_id', '=', 'False'),
        #                                ('company_id', 'child_of', [user.company_id.id])]})