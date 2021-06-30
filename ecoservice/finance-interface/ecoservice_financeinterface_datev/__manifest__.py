# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.
{
    'name': 'Finance Interface DATEV',
    'summary': 'Export of account moves to DATEV',
    'version': '13.0.1.2.1',
    'author': 'ecoservice',
    'website': 'https://ecoservice.de/shop/product/odoo-datev-export-53',
    'live_test_url': 'https://eco-finance-interface-13-0.test.ecoservice.de/',
    'support': 'financeinterface@ecoservice.de',
    'license': 'OPL-1',
    'category': 'Accounting',
    'images': [
        'images/main_screenshot.png',
    ],
    'depends': [
        'ecoservice_financeinterface',
    ],
    'data': [
        'data/ir_sequence.xml',

        # action used in res_config_view
        'wizards/views/ecofi_move_migration.xml',

        'views/account/account_account.xml',
        'views/account/account_move_line.xml',
        'views/account/account_tax.xml',
        'views/ecofi/ecofi.xml',
        'views/ecofi/ecofi_validation.xml',
        'views/res/res_config_settings.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
