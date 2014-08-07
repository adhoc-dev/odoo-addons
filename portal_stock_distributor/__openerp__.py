# -*- coding: utf-8 -*-
{
    'name': 'Portal Distributor Stock',
    'version': '0.1',
    'category': 'Tools',
    'complexity': 'easy',
    'description': """
Portal Stock Distributor Sale
=======================
    """,
    'author': 'Ingenieria ADHOC',
    'web': 'www.ingadhoc.com',
    'depends': ['portal_sale_distributor','portal_stock'],
    'demo': [
    ],
    'data': [
        'security/portal_security.xml',
        'security/ir.model.access.csv',
        'portal_sale_view.xml',
    ],
    'auto_install': True,
    'category': 'Hidden',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
