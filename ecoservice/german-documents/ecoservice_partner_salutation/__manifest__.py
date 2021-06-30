# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'Partner Salutation',
    'summary': 'Adds a salutation to the partner title.',
    'version': '13.0.1.0.0',
    'author': 'ecoservice',
    'website': 'https://www.ecoservice.de',
    'license': 'OPL-1',
    'category': 'Base',
    'depends': [
        'base',
    ],
    'data': [
        'static/src/sql/de.sql',
        'views/res_partner_view.xml',
        'data/res_partner_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
