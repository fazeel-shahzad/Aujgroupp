# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'ecoservice: Partner Account',
    'summary': 'New debit and credit account following a sequence per company for partner.',
    'version': '13.0.2.0.3',
    'author': 'ecoservice',
    'website': 'https://www.ecoservice.de',
    'license': 'OPL-1',
    'category': 'Accounting & Finance',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',  # security first
        'views/partner_account_configuration_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/menu_action.xml',  # menu last
    ],
    'post_init_hook': 'post_init_hook',
    'application': False,
    'auto_install': False,
    'installable': True,
}
