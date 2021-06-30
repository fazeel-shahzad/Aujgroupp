# -*- coding: utf-8 -*-
{
    'name': "so_tax_invoice",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Erum Asghar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

  
    'depends': ['base','sale','discount_account_invoice','universal_tax','sale_order_payment','discount_sale_order'],

    
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        'reports/report_so_tax.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
