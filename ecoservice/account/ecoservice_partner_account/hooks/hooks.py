# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """
    Migrates data from old module (ecoservice_partner_account_company).

    Except some field renaming, everything is generated automatically
    on install or now computed.

    This includes the configuration (sequence and account template) and
    the visibility of the buttons in res.partner to generate new accounts.
    """

    env = api.Environment(cr, SUPERUSER_ID, {})  # cr, uid, context

    old_module = env['ir.module.module'].search(
        [('name', '=', 'ecoservice_partner_account_company'),
         ('state', '=', 'installed')], limit=1)
    if old_module:
        # copy data of renamed fields to new ones
        query = """
        UPDATE res_company
        SET partner_account_generate_automatically = partner_generate_auto,
            partner_account_generate_multi_company = partner_generate_multicompany,
            partner_account_account_code_ref = partner_set_account_code_as_ref;
        """
        cr.execute(query)
        old_module.module_uninstall()
        old_module.unlink()

    # generate configuration
    env['res.company'].search([]).create_partner_account_configuration()
