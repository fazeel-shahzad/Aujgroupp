# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Product Article and Finish',

    'description': """
    Product Article No, Finish No And Filter for Article No, Finish No and Product in Sale, Purchase and Account
""",
    'version' : '1.0',
    'category': 'product',

    # Dependencies

    'depends' : ['product', 'sale', 'sale_management', 'purchase', 'account'],
    'license': 'OPL-1',
    # Views

    'data': [
        'views/product.xml',
    ],
    # Technical
    'installable': True,
    'currency': 'EUR',
    'auto_install': False,
    'application': True,
}
