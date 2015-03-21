# -*- coding: utf-8 -*-
{
    "name": "Database Tools",
    "version": "1.0",
    'author':  'ADHOC SA',
    'website': 'www.ingadhoc.com',
    # "category": "Accounting",
    "description": """
Database Tools
==============
TODO
    """,
    'depends': [
        'base'
        ],
    'data': [
        'wizard/database_tools_view.xml',
        'views/database_backup_view.xml',
        'views/database_view.xml',
        'backup_data.xml',
        'security/ir.model.access.csv',
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
    'auto_install': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
