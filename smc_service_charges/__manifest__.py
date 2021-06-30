# -*- coding: utf-8 -*-
{
    'name': "SMC Service Charges",

    'summary': """
        SMC Service Charges""",

    'description': """
        Add Service Charges with Installment Amount
    """,

    'author': "Atif Ali",
    'website': "http://www.abc.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/service_charges_views.xml',
    ],

}
