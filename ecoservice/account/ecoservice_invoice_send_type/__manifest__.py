# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the top level of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'ecoservice: Invoice Send Type',
    'summary': 'Determine the way of sending invoice. Selecting a type restricts the way of sending invoice to this customer.',
    'version': '13.0.1.0.1',
    'author': 'ecoservice',
    'website': 'https://ecoservice.de',
    'category': 'Base',
    'license': 'OPL-1',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'views/account/move_view.xml',
        'views/res/partner_view.xml',
    ],
    'installable': True,
}
