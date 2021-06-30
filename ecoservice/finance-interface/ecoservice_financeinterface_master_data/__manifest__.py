# Developed by ecoservice (Uwe Böttcher und Falk Neubert GbR).
# See COPYRIGHT and LICENSE files in the root directory of this module for full details.
{
    # App Information
    'name': 'Datev Master Data Export',
    'summary': 'Lets you export your accounting master data',
    'category': 'Accounting',
    'version': '13.0.1.1.2',
    'license': 'OPL-1',
    'application': False,
    'installable': True,
    # Author
    'author': 'ecoservice',
    'website': 'https://ecoservice.de/shop/product/odoo-datev-export-53',
    # Odoo Apps Store
    'support': 'financeinterface@ecoservice.de',
    # Dependencies
    'depends': [
        'account',
        'base',

        'ecoservice_financeinterface',  # eco/finance-interface
    ],
    # Data
    'data': [
        'security/ir.model.access.csv',
        'data/datev_export_data.xml',
        'views/datev_export.xml',
        'wizards/export_ecofi_datev_export.xml',
    ],
}
