# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'ecoservice: MAGU Bausysteme GmbH',
    'summary': 'Customizations for MAGU Bausysteme GmbH.',
    'version': '13.0.1.2.0',
    'author': 'ecoservice',
    'website': 'https://www.ecoservice.de',
    'license': 'LGPL-3',
    'category': 'Base',
    'depends': [
        'sale',
        'ecoservice_german_documents_base',
        'ecoservice_german_documents_sale',
    ],
    'data': [
        'data/mail_data.xml',
        'reports/german_documents/base/report_base.xml',
        'reports/german_documents/base/report_css.xml',
        'reports/german_documents/sale/document.xml',
        'reports/german_documents/sale/order.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
