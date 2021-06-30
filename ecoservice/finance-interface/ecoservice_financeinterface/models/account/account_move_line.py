# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import _, api, exceptions, fields, models


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit = [
        'account.move.line',
        'ecofi.validation.mixin',
    ]

    # region Fields
    ecofi_tax_id = fields.Many2one(
        comodel_name='account.tax',
        string='Move Tax',
    )
    ecofi_account_counterpart = fields.Many2one(
        string='Account Counterpart',
        comodel_name='account.account',
        ondelete='restrict',
    )
    # endregion

    # region Constraints
    @api.constrains('tax_ids')
    def _check_tax_ids(self):
        for line in self.filtered(lambda l: l.company_id.uses_skr()):
            if len(line.tax_ids) > 1:
                raise exceptions.ValidationError(_(
                    'Error! There can only be one tax per invoice line.'
                ))
    # endregion

    # region CRUD Methods
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            tax_ids = vals.get('tax_ids') or []  # tax_ids can be False
            if not vals.get('ecofi_tax_id') and tax_ids and tax_ids[0][2]:
                # account.payment transfers the actual ids in a set
                vals['ecofi_tax_id'] = list(tax_ids[0][2])[0]
        return super().create(vals_list)
    # endregion

    # region Business Methods
    def _ecofi_validations_enabled(self):
        return self.move_id._ecofi_validations_enabled()

    def name_get(self):
        if self.env.context.get('counterpart_name'):
            result = []
            for line in self:
                if line.ref:
                    result.append(
                        (line.id, (line.name or '') + ' (' + line.ref + ')'),
                    )
                else:
                    result.append((line.id, line.name))
            return result
        return super(AccountMoveLine, self).name_get()

    @api.ecofi_validate('validate_tax_count')
    def _validate_tax_count(self):
        """Check if there is at most one tax in the line."""

        self.ensure_one()

        is_valid = len(self.tax_ids) <= 1
        if not is_valid:
            raise exceptions.ValidationError(_('More than one tax specified!'))
    # endregion
