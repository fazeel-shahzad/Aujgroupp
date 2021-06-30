# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup_multi_company import BaseSetupMultiCompany


class TestAutomaticAccountCreationMultiCompanyShared(BaseSetupMultiCompany):
    """
    Since the automatic creation of accounts calls the same methods as the
    manual creation we just don't need to have specific tests for those
    """
