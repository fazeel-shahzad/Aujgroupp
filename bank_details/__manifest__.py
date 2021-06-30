# -*- coding: utf-8 -*-
{
    'name': "Bank Details",

    'summary': """
        Vendor XLSX Report""",

    'description': """
        Report
    """,

    'author': "Atif Ali",
    'website': "http://www.abc.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'report/report.xml',
        # 'views/partner.xml',
    ],
}
