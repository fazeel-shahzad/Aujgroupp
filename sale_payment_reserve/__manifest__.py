# -*- coding: utf-8 -*-
{
    'name': "Sale Payment Reserve",

    'summary': """
        Sale Payment Reserve""",

    'description': """
        Sale Payment Reserve
    """,

    'author': "Atif Ali",
    'website': "http://www.atif.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'branch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'wizards/advance_payment_wizard.xml',
    ],

}
