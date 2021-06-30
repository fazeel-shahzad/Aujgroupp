# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'German Documents (Base)',
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
        'base',
        'web',
        'ecoservice_partner_salutation',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/paperformat.xml',
        'reports/report_base.xml',  # don't change the order of this file
        'data/report_layout.xml',
        'reports/report_css.xml',
        'reports/report_snippets.xml',
        'reports/report_snippets_letterhead_reference.xml',
        'views/res_company_view.xml',
        'views/res_config_view.xml',
        'views/text_template_config.xml',
    ],
    'installable': True,
    'price': 550.00,
    'currency': 'EUR',
}
