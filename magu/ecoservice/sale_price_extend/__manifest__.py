# Part of AktivSoftware
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Price Extended',
    'version': '13.0.1.0.1',
    'category': 'Sales',
    'summary': 'Sale Price Customization',
    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",
        'license': 'LGPL-3',
    'depends': [
        'sale',
        'product',
        'sale_management',
    ],
    'data': [
        'views/product_pricelist_view.xml',
        'views/sale_views.xml',
        'wizard/sale_order_line_product_price_wizard.xml',
    ],

    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
}
