# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_de_datev_consultant_number = fields.Char(company_dependent=False)
    l10n_de_datev_client_number = fields.Char(company_dependent=False)
