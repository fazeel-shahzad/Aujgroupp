# # Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.


def migrate(cr, version):
    if not version:
        return

    cr.execute("""
        CREATE TABLE IF NOT EXISTS account_tax_rel (
            account_id integer,
            tax_id integer,

            CONSTRAINT account_tax_rel_account_id_tax_id_key
                PRIMARY KEY(account_id, tax_id),
            CONSTRAINT account_tax_rel_account_id_fkey
                FOREIGN KEY (account_id)
                REFERENCES account_account(id)
                ON DELETE CASCADE,
            CONSTRAINT account_tax_rel_tax_id_fkey
                FOREIGN KEY (tax_id)
                REFERENCES account_tax(id)
                ON DELETE CASCADE
        );
    """)

    cr.execute("""
        INSERT INTO account_tax_rel
        (
            SELECT
                aa.id,
                aa.datev_steuer
            FROM account_account AS aa
            WHERE aa.datev_steuer IS NOT NULL
        );
    """)

    cr.commit()
