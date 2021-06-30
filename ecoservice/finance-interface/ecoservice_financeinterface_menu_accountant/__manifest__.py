# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

# noinspection PyStatementEffect
{
    'name': 'Finance Interface Menu Accountant',
    'summary': 'Make the menu account_accountant (Enterprise module) compliant',
    'version': '13.0.1.0.0',
    'author': 'ecoservice',
    'website': 'https://ecoservice.de/shop/product/odoo-datev-export-53',
    'live_test_url': 'https://eco-finance-interface-13-0.test.ecoservice.de/',
    'support': 'financeinterface@ecoservice.de',
    'license': 'OPL-1',
    'category': 'Accounting',
    'depends': [
        'account_accountant',
        'ecoservice_financeinterface',
    ],
    'data': [
        'views/menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': True,
}
