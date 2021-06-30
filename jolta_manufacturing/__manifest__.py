# -*- coding: utf-8 -*-
{
    'name': "Jolta Manufacturing",

    'summary': """
        Jolta Manufacturing""",

    'description': """
        Jolta Manufacturing
    """,

    'author': "Atif",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'material_purchase_requisitions', 'mrp', 'stock', 'purchase','parent_sku'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'report/requisition_report.xml',
        'report/stock_report.xml',
        'report/quality_report.xml',
        'report/internal_transfer_report.xml',
        'report/immediate_transfer_report.xml',
        'views/views.xml',
    ],
}
