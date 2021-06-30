# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from .base_setup import BaseSetup


class BaseSetupMultiCompany(BaseSetup):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.company_2 = cls.RC.create({
            'name': 'Daily Planet',
        })
        cls.company_3 = cls.RC.create({
            'name': 'Umbrella Corporation',
        })

        # make sure that all companies have accounts
        # company 1 has them set by default after installing a coa
        cls.account_chart.try_loading(cls.company_2)
        cls.account_chart.try_loading(cls.company_3)
