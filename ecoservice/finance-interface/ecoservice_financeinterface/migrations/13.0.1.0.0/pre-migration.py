# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.


def migrate(cr, version):
    if not version:
        return

    cr.execute("""ALTER TABLE account_move_line RENAME COLUMN ecofi_taxid TO ecofi_tax_id;""")  # noqa: E501
    cr.execute("""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT *
                FROM   information_schema.columns
                WHERE  table_name='account_move'
                AND    column_name='datev_checks_enabled'
            )
            THEN
                ALTER TABLE   "public"."account_move"
                RENAME COLUMN "datev_checks_enabled" TO "ecofi_validations_enabled";
            END IF;
        END $$;
    """)

    cr.commit()
