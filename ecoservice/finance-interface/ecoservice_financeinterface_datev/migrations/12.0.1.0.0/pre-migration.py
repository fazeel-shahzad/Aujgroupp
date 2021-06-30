# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.


def migrate(cr, version):
    if not version:
        return

    # Rename some fields but don't change their content
    cr.execute("""ALTER TABLE account_account    RENAME COLUMN ustuebergabe               TO datev_vat_handover;""")  # noqa: E501
    cr.execute("""ALTER TABLE account_account    RENAME COLUMN automatic                  TO datev_automatic_account;""")  # noqa: E501
    cr.execute("""ALTER TABLE account_account    RENAME COLUMN datev_steuer               TO datev_tax_ids;""")  # noqa: E501
    cr.execute("""ALTER TABLE account_account    RENAME COLUMN datev_steuer_erforderlich  TO datev_tax_required;""")  # noqa: E501
    cr.execute("""ALTER TABLE account_invoice    RENAME COLUMN enable_datev_checks        TO datev_checks_enabled;""")  # noqa: E501
    cr.execute("""ALTER TABLE account_move_line  RENAME COLUMN ecofi_bu                   TO datev_posting_key;""")  # noqa: E501
    cr.execute("""ALTER TABLE account_tax        RENAME COLUMN datev_skonto               TO datev_cashback_account_id;""")  # noqa: E501
    cr.execute("""ALTER TABLE res_company        RENAME COLUMN enable_datev_checks        TO datev_checks_enabled;""")  # noqa: E501

    # Create a new column for the renamed field
    cr.execute("""
        ALTER TABLE res_company
        ADD COLUMN IF NOT EXISTS datev_export_method VARCHAR;
    """)

    # Insert renamed data in the renamed field
    cr.execute("""
        UPDATE res_company
        SET datev_export_method =
            CASE WHEN exportmethod = 'brutto' THEN 'gross'
                 WHEN exportmethod = 'netto'  THEN 'net'
                 ELSE 'gross'
            END;
    """)

    cr.commit()
