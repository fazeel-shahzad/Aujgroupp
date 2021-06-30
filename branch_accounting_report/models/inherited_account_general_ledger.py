# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from datetime import  timedelta
from odoo.tools import float_is_zero

class report_account_general_ledger(models.AbstractModel):
    _inherit = "account.general.ledger"

    filter_branch = True

    @api.model
    def _get_options_domain(self, options):
        domain = super(report_account_general_ledger, self)._get_options_domain(options)

        if options.get('branch') and options.get('branch_ids'):
            domain += [
                ('branch_id','in',options.get('branch_ids') )
            ]

        return domain