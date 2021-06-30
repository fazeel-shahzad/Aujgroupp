{
    'name': 'Manage User Sales Commission',
    'version': '13.0',
    'category': 'Sales',
    'license': 'OPL-1',
    'summary': 'Create your own Commission Structure and Manage Sales Commission.',

    'author': 'Er. Vaidehi Vasani',
    'maintainer': 'Er. Vaidehi Vasani',

    'images': ['static/description/user_sales_commission_app_coverpage.jpg'],

    'depends': ['sale'],
    'data': [
        'security/user_sales_commission_security.xml',
        'security/ir.model.access.csv',
        'wizard/generate_commission_view.xml',
        'views/res_users_inherit_view.xml',
        'views/sale_order.xml',
        'views/commission_config_view.xml',
        'views/sale_order_commission_view.xml',
        'views/menuitems.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 0.00,
    'currency': 'EUR',
}
