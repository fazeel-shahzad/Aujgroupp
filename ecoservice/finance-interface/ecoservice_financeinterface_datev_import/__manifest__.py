# -*- coding: utf-8 -*-
# Part of Odoo. Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE at the root directory of this module for full copyright and licensing details.

{
    'name': 'Financial Interface DATEV Import',
    'summary': 'This module allows you to import accounting entries.',
    'version': '13.0.1.0.0',
    'author': 'ecoservice',
    'website': 'https://ecoservice.de/shop/product/odoo-datev-export-53',
    'live_test_url': 'https://eco-finance-interface-13-0.test.ecoservice.de/',
    'support': 'financeinterface@ecoservice.de',
    'licence': 'OPL-1',
    'category': 'Accounting',
    'depends': [
        'base',
        'account',
        'ecoservice_financeinterface',
        'ecoservice_financeinterface_datev',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/import_datev_sequence.xml',
        'views/import_datev.xml',
        'views/import_datev_menu.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
