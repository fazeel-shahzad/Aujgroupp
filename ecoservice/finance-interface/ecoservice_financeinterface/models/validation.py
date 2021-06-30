# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from functools import wraps
from typing import Callable

from odoo import api

OptionField = str


class Condition:
    def __init__(self, *conditions) -> None:
        self._conditions = conditions

    def __call__(self, record) -> bool:
        raise NotImplementedError


class AnyOf(Condition):
    def __call__(self, record) -> bool:
        return any(cond(record) for cond in self._conditions)


class AllOf(Condition):
    def __call__(self, record) -> bool:
        return all(cond(record) for cond in self._conditions)


class OneOf(Condition):
    def __call__(self, record) -> bool:
        return sum(cond(record) for cond in self._conditions) == 1


class NoneOf(Condition):
    def __call__(self, record) -> bool:
        return not any(cond(record) for cond in self._conditions)


def ecofi_validate(option: OptionField, *conditions: Condition) -> Callable:
    """
    Execute a validation method when a precondition is met.

    Note that this is different from real preconditions/contracts as those stop
    the flow when a precondition fails. In this case we just don't want a
    validation to be executed when a precondition is not met.

    .. The conditions must be of the form::

        accumulation_function(condition1, condition2, ...)

    Where the accumulation_function can be one of
        'any_of', 'all_of', 'one_of', 'none_of'
    These functions are registered in the odoo.api namespace.

    .. Example::

        class AccountMove(Model):

            @api.ecofi_validate(
                'validate_tax_is_set',
                api.any_of(
                    lambda self: self.account_id.datev_automatic_account,
                    lambda self: self.account_id.tax_required,
                ),
                api.none_of(
                    _is_tax_line,
                ),
            )
            def _validate_tax_is_set(self):
                pass

    :param option: Field in ecofi.validation
    :param conditions: Callables that will be evaluated before execution
    """
    if not conditions:
        return api.attrsetter('_ecofi_validate', option)

    def null_function(*_):
        pass

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args):
            if all(cond(self) for cond in conditions):
                return func(self, *args)
            return null_function(self, *args)

        setattr(wrapper, '_ecofi_validate', option)
        return wrapper
    return decorator


api.ecofi_validate = ecofi_validate
api.any_of = AnyOf
api.all_of = AllOf
api.one_of = OneOf
api.none_of = NoneOf
