# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'ecoservice: UOM Conversion on German Documents',
    'summary': 'Display UOM Conversion on German Documents.',
    'version': '13.0.1.0.0',
    'author': 'ecoservice',
    'website': 'https://www.ecoservice.de',
    'license': 'LGPL-3',
    'category': 'Sales/Sales',
    'depends': [
        'ecoservice_german_documents_all',
        'ecoservice_uom_conversion',
    ],
    'data': [
        'reports/report_invoice_uom_table.xml',
        'reports/report_sale_uom_table.xml',
        'reports/report_stock_uom_table.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
