# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.


def migrate(cr, installed_version):
    if not installed_version:
        return

    sql = """
        UPDATE res_company
        SET partner_account_account_code_ref_preferred = 'receivable'
        WHERE partner_account_account_code_ref_preferred = 'customer';
        UPDATE res_company
        SET partner_account_account_code_ref_preferred = 'payable'
        WHERE partner_account_account_code_ref_preferred = 'supplier';
    """
    cr.execute(sql)

    sql = """
        SELECT SUM(CAST(partner_account_account_code_ref as int))
        FROM res_company;
    """

    cr.execute(sql)
    result = cr.fetchone()
    if result and result[0] and result[0] > 0:
        sql = """
        INSERT INTO ir_config_parameter
            (key, value, create_date, write_date, create_uid, write_uid)
        VALUES
            ('partner_account.set_ref_on_account_creation', 'True', now(), now(), 1, 1)
        ON CONFLICT DO NOTHING;
        """
        cr.execute(sql)
