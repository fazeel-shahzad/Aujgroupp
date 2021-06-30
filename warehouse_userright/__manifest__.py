# -*- coding: utf-8 -*-
{
    'name': "Warehouse User Right",

    'summary': """
        Warehouse User Right""",

    'description': """
        Adding New fields Driver, mobile, vehicle no etc.
        Remove Create and other header button in waiting state on 'Remove Create Button' group on user form.
        Show sum of Reserved, Forecasted, Done Quantity.
        On Change Adding reserve quantity to done quantity. 
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
    ],

}
