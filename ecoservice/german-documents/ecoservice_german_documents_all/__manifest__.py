# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'German Documents',
    'summary': 'Designed German Documents for Odoo.',
    'version': '13.0.1.0.0',
    'author': 'ecoservice',
    'website': 'https://www.ecoservice.de/shop/product/deutsche-dokumente-fur-odoo-47',
    'live_test_url': 'https://eco-german-documents-13-0.test.ecoservice.de/',
    'support': 'deutsche-dokumente@ecoservice.de',
    'license': 'OPL-1',
    'category': 'Base',
    'images': [
        'images/main_screenshot.png',
    ],
    'depends': [
        'ecoservice_german_documents_base',
        'ecoservice_german_documents_invoice',
        'ecoservice_german_documents_purchase',
        'ecoservice_german_documents_sale',
        'ecoservice_german_documents_stock',
    ],
    'data': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
