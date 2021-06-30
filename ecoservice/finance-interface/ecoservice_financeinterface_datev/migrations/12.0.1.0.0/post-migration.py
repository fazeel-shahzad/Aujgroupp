# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.


def migrate(cr, version):
    if not version:
        return

    # Remove the old field which was renamed
    cr.execute("""
        ALTER TABLE res_company
        DROP COLUMN IF EXISTS exportmethod;
    """)

    cr.commit()
