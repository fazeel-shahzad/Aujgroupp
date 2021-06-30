# -*- coding: utf-8 -*-
{
    'name': "Remove Quick Create and Edit",

    'summary': """
        Remove Quick Create and Edit""",

    'description': """
        Remove Quick Create and Edit from Sale, Purchase, Account
    """,

    'author': "Atif Ali",
    'website': "http://www.abc.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/purchase_views.xml',
        'views/account_views.xml',
    ],
    # # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
