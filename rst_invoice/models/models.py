# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInheritRights(models.Model):
    _inherit = 'account.move'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        # if self.env.user.id != 2 and self.env.user.has_group('rst_invoice.group_own_invoce_custom'):
        if  self.env.user.has_group('rst_invoice.group_own_invoce_custom'):
            args += [('invoice_user_id','=',self.env.user.id),('state','=','posted')]
        return super(AccountMoveInheritRights, self)._search(args, offset=offset, limit=limit, order=order,
                                                           count=count, access_rights_uid=access_rights_uid)
