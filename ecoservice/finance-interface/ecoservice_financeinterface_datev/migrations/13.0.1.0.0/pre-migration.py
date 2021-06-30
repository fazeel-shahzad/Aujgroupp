# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

from contextlib import suppress


def migrate(cr, version):
    if not version:
        return

    column_mapping = [
        ('buchungsschluessel', 'l10n_de_datev_code'),
        ('datev_client_no', 'l10n_de_datev_client_number'),
        ('datev_consultant_no', 'l10n_de_datev_consultant_number'),
    ]
    for column_map in column_mapping:
        with suppress(Exception):
            cr.execute("""
                UPDATE account_tax
                SET %(new)s=%(old)s;
            """, {
                'old': column_map[0],
                'new': column_map[1],
            })

    cr.commit()
