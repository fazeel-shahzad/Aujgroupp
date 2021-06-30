# -*- coding: utf-8 -*-
{
    'name': 'Hide Edit Option for specific users/groups',
    'version': '11.0.1.0',
    'license': 'Other proprietary',
    'category': 'Sales',
    'summary': """This app provide option to hide "Edit" button for specific user and user group.
                    After selecting this option user will not be able to see edit button.
                    Keywords
                    hide edit remove edit no edit allowed edit form list kanban
                """,
    'author':'Craftsync Technologies',
    'maintainer': 'Craftsync Technologies',
    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'sequence': 1,
    'depends': [
        'base','web'
    ],
    'data': [
        'security/import_security.xml',
        'views/res_groups.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 15.00,
    'currency': 'EUR',
 }