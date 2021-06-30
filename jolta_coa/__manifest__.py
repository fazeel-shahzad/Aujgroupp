# -*- coding: utf-8 -*-
{
    'name': "jolta_coa",

    'summary': """
       Chart of Accounts""",

    'description': """
       step one:install jolta_coa
       step two: install accounting 
    """,

    'author': "Erum Asghar",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','l10n_generic_coa','account_parent'],

    # always loaded
    'data': [
        #'security/account.account.template.csv',

        'demo/demo.xml',
        'demo/account.account.template.csv'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
