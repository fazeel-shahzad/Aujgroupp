# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    cr.execute("""
        ALTER TABLE res_company
        ADD COLUMN IF NOT EXISTS l10n_de_datev_consultant_number VARCHAR;

        ALTER TABLE res_company
        ADD COLUMN IF NOT EXISTS l10n_de_datev_client_number VARCHAR;
    """)
    for company in env['res.company'].search([]):
        cr.execute("""
            UPDATE res_company
            SET (
                l10n_de_datev_consultant_number,
                l10n_de_datev_client_number,
            ) = (
                %(consultant)s,
                %(client)s,
            )
            WHERE id=%(id)s;
        """, {
            'consultant': company.l10n_de_datev_consultant_number,
            'client': company.l10n_de_datev_client_number,
            'id': company.id,
        })

    cr.commit()
