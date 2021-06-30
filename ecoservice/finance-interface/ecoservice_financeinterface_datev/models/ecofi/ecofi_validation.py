# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class EcofiValidation(models.Model):
    _inherit = 'ecofi.validation'
    _description = 'En- or disable specific checks company-wide'

    # region Fields
    # account.move
    validate_account_counter_account = fields.Boolean(
        default=True,
        help='Validates that the account and counter account moves are balanced.',
    )
    # account.move.line
    validate_required_tax_is_set = fields.Boolean(
        default=True,
        help='Validates that the tax in a line is set if the related account requires it.',  # noqa: E501
    )
    validate_automatic_account_has_tax = fields.Boolean(
        default=True,
        help='Validates that an account that requires a tax has configured at least one.',  # noqa: E501
    )
    validate_automatic_account_line_has_correct_tax = fields.Boolean(
        default=True,
        help='Validates that the tax in a line is one of those that are configured in the related account.',  # noqa: E501
    )
    validate_tax_booking_key_is_set = fields.Boolean(
        default=True,
        help='Validates that the tax in a line has set any booking key/datev code.',  # noqa: E501
    )
    # endregion
