# -*- coding: utf-8 -*-
{
    'name': "Sale Customer Report",

    'summary': """
        Sale Customer Report""",

    'description': """
        Sale Customer Report
    """,

    'author': "Atif Ali",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_customer_report_wizard.xml',
        'report/sale_customer_report.xml',
    ],

}
