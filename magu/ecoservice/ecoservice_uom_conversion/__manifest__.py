# Extension of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

# noinspection PyStatementEffect
{
    'name': 'ecoservice: UOM Conversion',
    'summary': 'Add UOM Category including the specified UOMs and its default values.',
    'version': '13.0.1.0.0',
    'author': 'ecoservice',
    'website': 'https://www.ecoservice.de',
    'license': 'LGPL-3',
    'category': 'Sales/Sales',
    'depends': [
        'sale_management',
        'sale_stock',
    ],
    'data': [
        'data/uom_data.xml',
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/stock_move_line_views.xml',
        'views/uom_views.xml',
        'reports/report_deliveryslip.xml',
        'reports/report_invoice.xml',
        'reports/report_stockpicking_operations.xml',
        'reports/sale_report_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
