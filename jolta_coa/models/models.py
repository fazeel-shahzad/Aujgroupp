# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class jolta_coa(models.Model):
    _inherit = 'account.account'

    def get_latest_code(self,parent_id):
        self.code = ''
        if self.parent_id and self.parent_id.code:
            self.code = ''
            if self.parent_id.parent_id  and not self.parent_id.parent_id.parent_id:

                previous_code = self.env['account.account'].search([])
                previous_codes = self.env['account.account'].search([('parent_id', '=', parent_id.id)])
                prev_codes_list = [x.code for x in previous_codes]

                if prev_codes_list:
                    prev_codes_list = sorted(prev_codes_list)
                    prev_latest_code = prev_codes_list[-1].split('-')
                    latest_code = int(prev_codes_list[-1].split('-')[-1])
                    new_code = str(latest_code + 1)
                    account_code = ''

                    account_code = new_code.zfill(4)
                    prev_latest_code.remove(prev_latest_code[-1])
                    prev_latest_code.append(account_code)
                    new_latestaccount_code = '-'.join(prev_latest_code)
                    return new_latestaccount_code
                else:
                    parent_code = self.parent_id.code
                    latest_code_split = self.parent_id.code.split('-')
                    next_code = str(int(self.parent_id.code.split('-')[-1]) + 1).zfill(4)
                    latest_code_split.remove(latest_code_split[-1])
                    latest_code_split.append(next_code)
                    new_latestaccount_code = '-'.join(latest_code_split)
                    return new_latestaccount_code




    @api.onchange('parent_id')
    def update_account_code(self):
        if self.parent_id:
            acc_code=''
            acc_code= self.get_latest_code(self.parent_id)
            self.code = acc_code








