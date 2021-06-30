# -*- coding: utf-8 -*-
{
    'name': "Employee Payroll Report",
    'summary': """Employee PayrolL PDF report with some inherit fields""",
    'description': """ This module will print the pdf report of the Employee payroll and we
                        inherited fields also""",
    'author': "Imran",
    'website': "http://www.yourcompany.com",
    'category': 'Employee',
    'version': '0.1',
    'depends': ['base','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'reports/payroll_pdf_template.xml',
        'reports/payroll_report.xml',
        'views/payroll_style.xml',

    ],
    'demo': [
        'demo/demo.xml',
    ],
}
