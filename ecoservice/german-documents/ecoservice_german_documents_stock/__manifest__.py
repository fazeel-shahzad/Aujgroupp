# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'German Documents (Stock)',
    'summary': 'Designed German Documents for Odoo.',
    'version': '13.0.1.2.2',
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
        'stock',
        'ecoservice_german_documents_base',
    ],
    'data': [
        'reports/report_stock.xml',
        'reports/report_stock_css.xml',
        'reports/report_stock_document_delivery_note.xml',
        'reports/report_stock_document_picking_operation.xml',
        'reports/report_stock_snippets.xml',
        'reports/report_stock_table.xml',
    ],
    'installable': True,
}
