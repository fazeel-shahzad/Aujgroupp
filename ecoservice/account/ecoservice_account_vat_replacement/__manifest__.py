# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files at the root directory for full details.

# noinspection PyStatementEffect
{
    'name': 'ecoservice: VAT Replacement',
    'summary': 'Configure and execute a tax and account replacement configuration',
    'version': '13.0.1.0.1',
    'author': 'ecoservice',
    'website': 'https://ecoservice.de',
    'category': 'Account',
    'license': 'OPL-1',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/vat_configuration.xml',
        'views/menu.xml',
    ],
    'installable': True,
}
