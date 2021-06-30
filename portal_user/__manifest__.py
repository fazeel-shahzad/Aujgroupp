# -*- coding: utf-8 -*-
{
    'name': "portal_user",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/user_dashboard.xml',
        'views/portal_template.xml',
        'views/attendance.xml',
        'views/attendance_view.xml',
        'views/my_time_off_request.xml',
        'views/time_off_view.xml',
        'views/my_allocation_request.xml',
        'views/allocation_view.xml',
        'views/request_for_loan_form.xml',
        'views/loanrequest_view.xml',
        'views/advance_salary.xml',
        'views/advance_salary_view.xml',
        'views/web.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
