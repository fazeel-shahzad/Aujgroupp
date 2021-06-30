# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import _, api, exceptions, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # region Fields
    datev_export_value = fields.Monetary(
        string='Export value',
    )
    datev_posting_key = fields.Selection(
        selection=[
            ('40', '40'),
            ('SD', 'Steuer Direkt'),
        ],
        string='Datev BU',
    )
    # endregion

    # region Getter
    def get_tax(self):
        """
        Return the used tax.
        """
        self.ensure_one()
        return (
            self.tax_ids
            or self.ecofi_tax_id
            or self.env['account.tax']
        )
    # endregion

    # region Business Methods
    def _datev_is_automatic_account(self) -> bool:
        return self.account_id.datev_automatic_account

    def _datev_is_tax_required(self) -> bool:
        return self.account_id.datev_tax_required

    def _datev_is_credit_line(self) -> bool:
        return (
            self.account_id != self.ecofi_account_counterpart
            and not (
                self.account_id.is_tax_account()
                or self.datev_posting_key != 'SD'
            )
        )

    def _datev_has_tax(self) -> bool:
        return bool(self.get_tax())

    @api.ecofi_validate(
        'validate_required_tax_is_set',
        api.any_of(
            _datev_is_credit_line,
            _datev_is_tax_required,
        ),
    )
    def _validate_required_tax_is_set(self):
        self.ensure_one()

        is_valid = self.get_tax()
        if not is_valid:
            raise exceptions.ValidationError(
                _(
                    'The account {account} requires a tax to be set in the line'
                    ' but no tax is set!'
                ).format(
                    account=self.account_id.code,
                    debit=self.debit,
                    credit=self.credit,
                )
            )

    @api.ecofi_validate(
        'validate_automatic_account_has_tax',
        api.any_of(
            _datev_is_automatic_account,
            _datev_is_tax_required,
        ),
    )
    def _validate_required_tax_is_set(self):
        self.ensure_one()

        is_valid = self._datev_has_tax()
        if not is_valid:
            raise exceptions.ValidationError(
                _(
                    'The account requires a tax but no tax is set!'
                ).format(
                    account=self.account_id.code,
                    debit=self.debit,
                    credit=self.credit,
                )
            )

    @api.ecofi_validate(
        'validate_automatic_account_line_has_correct_tax',
        api.all_of(_datev_is_automatic_account),
    )
    def _validate_automatic_account_line_has_correct_tax(self):
        self.ensure_one()

        # Don't use self.get_tax() as we must make sure that standard tax
        # is set correctly
        is_valid = self.tax_ids in self.account_id.datev_tax_ids
        if not is_valid:
            raise exceptions.ValidationError(
                _(
                    'The account {account} is an automatic account but'
                    ' the tax ({tax}) differs'
                    ' from the configured ({configured_taxes})!'
                ).format(
                    account=self.account_id.code,
                    tax=self.get_tax().description,
                    configured_taxes=', '.join(
                        self.mapped('account_id.datev_tax_ids.description'),
                    ),
                )
            )

    @api.ecofi_validate(
        'validate_tax_booking_key_is_set',
        api.all_of(_datev_has_tax),
    )
    def _validate_tax_booking_key_is_set(self):
        self.ensure_one()

        is_valid = bool(self.get_tax().l10n_de_datev_code)
        if not is_valid:
            raise exceptions.ValidationError(
                _(
                    'The booking key for the tax "{tax}" is not configured!'
                ).format(
                    tax=self.get_tax().name,
                )
            )

    # endregion
