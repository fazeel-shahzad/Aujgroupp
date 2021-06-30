# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from ..exceptions import FinanceinterfaceException


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = [
        'account.move',
        'ecofi.validation.mixin',
    ]

    # region Fields
    vorlauf_id = fields.Many2one(
        comodel_name='ecofi',
        string='Export',
        readonly=True,
        copy=False,
        ondelete='set null',
    )
    ecofi_buchungstext = fields.Char(
        string='Export Voucher Text',
        size=60,
    )
    ecofi_manual = fields.Boolean(
        string='Set Counter accounts manually',
    )
    ecofi_to_check = fields.Boolean(
        string='Verify',
    )
    ecofi_validations_enabled = fields.Boolean(
        string='Perform Validations',
        default=True,
    )
    # endregion

    # region CRUD Methods
    def unlink(self):
        """
        Prevent exported moves from being deleted.
        """
        for thismove in self:
            if self.env.context.get('delete_none', False):
                continue
            if thismove.vorlauf_id:
                raise FinanceinterfaceException(
                    _(
                        'Warning! Account moves which are already in an '
                        'export can not be deleted!'
                    )
                )
        return super(AccountMove, self).unlink()
    # endregion

    # region Action Methods
    def button_cancel(self):
        """
        Check if the move has already been exported.
        """
        res = super(AccountMove, self).button_cancel()
        for move in self:
            if move.vorlauf_id:
                raise FinanceinterfaceException(
                    _('Error! You cannot modify an already exported move.')
                )
        return res
    # endregion

    # region Business Methods
    def post(self):
        """
        Perform checks if a move is posted.
        """
        error_msg = self.perform_validations()
        if error_msg:
            raise ValidationError('\n\n'.join(error_msg))
        return super().post()

    def _ecofi_validations_enabled(self) -> bool:
        return self.ecofi_validations_enabled

    def perform_validations(self):
        result = super().perform_validations()
        for number, line in enumerate(self.line_ids, start=1):
            result.extend([
                _('Line {number}: {validation}').format(
                    number=number,
                    validation=validation,
                )
                for validation in line.perform_validations()
            ])
        return result

    # endregion
