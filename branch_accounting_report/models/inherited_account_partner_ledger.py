# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.tools import float_is_zero
from datetime import timedelta


class AccountPartnerLedger(models.AbstractModel):
    _inherit = 'account.partner.ledger'

    filter_branch = True

    @api.model
    def _get_options_domain(self, options):
        domain = super(AccountPartnerLedger, self)._get_options_domain(options)

        if options.get('branch') and options.get('branch_ids'):
            domain += [
                ('branch_id','in',options.get('branch_ids') )
            ]

        return domain
