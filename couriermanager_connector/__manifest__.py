# -*- coding: utf-8 -*-
{
    'name': "couriermanager_connector",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Hunain AK",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.6',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/cities.xml',
        'views/expedition_price.xml',
        'views/expedition_info.xml',
        'wizard/message_wizard.xml',
        'wizard/wizards.xml',
        'views/import_process.xml',
        'views/invoices.xml',
        'views/auto_importer.xml',
        'data/schedulers.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
