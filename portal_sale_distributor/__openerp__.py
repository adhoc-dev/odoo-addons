# -*- coding: utf-8 -*-
{
    'name': 'Portal Distributor Sale',
    'version': '0.1',
    'category': 'Tools',
    'complexity': 'easy',
    'description': """
Portal Distributor Sale
=======================
    """,
    'author': 'Ingenieria ADHOC',
    'web': 'www.ingadhoc.com',
    'depends': ['portal_sale'],
    'demo': [
        'portal_demo.xml',
    ],
    'data': [
        'security/portal_security.xml',
        'security/ir.model.access.csv',
        'portal_sale_view.xml',
    ],
    'auto_install': False,
    'application': True,
    'category': 'Hidden',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
