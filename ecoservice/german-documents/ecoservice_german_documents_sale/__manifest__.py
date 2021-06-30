# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'German Documents (Sale)',
    'summary': 'Designed German Documents for Odoo.',
    'version': '13.0.1.4.1',
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
        'sale_management',
        'ecoservice_german_documents_base','product_ext'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/text_template.xml',
        'reports/report_sale.xml',
        'reports/report_sale_css.xml',
        'reports/report_sale_document.xml',
        'reports/report_sale_snippets.xml',
        'reports/report_sale_table.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
}
