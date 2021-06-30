# -*- coding: utf-8 -*-
{
    'name': "Customer History",

    'summary': """
       Developed some basic information related to Customer History""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TABEER ASLAM (ODOO CONSULTANT BACKEND DEVELOPER)",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
