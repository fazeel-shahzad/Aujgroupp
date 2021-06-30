# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.
# noinspection PyStatementEffect
{
    'name': 'Finance Interface',
    'summary': 'Main and base module of the Finance Interface',
    'version': '13.0.1.1.2',
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
        'l10n_de',
    ],
    'data': [
        'security/ecofi_security.xml',
        'security/ir.model.access.csv',

        'data/ir_sequence.xml',

        'views/account/account_move.xml',
        'views/account/account_move_line.xml',
        'views/ecofi/ecofi.xml',
        'views/ecofi/ecofi_validation.xml',
        'views/res/res_config_settings.xml',

        'wizards/export_ecofi.xml',

        'views/action.xml',
        'views/menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'price': 550.00,
    'currency': 'EUR',
}
