# -*- coding: utf-8 -*-
{
    'name': "Sale Line images",

    'summary': """
    """,

    'description': """

    """,

    'author': "Bilal",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','ecoservice_german_documents_sale','portal','ecoservice_german_documents_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_report.xml',
        'views/sale_portal_templates.xml',
        'views/report_stock_image.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
