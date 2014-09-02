# -*- coding: utf-8 -*-
{
    'name': 'Sale Restrict Partners',
    'version': '1.0',
    'category': 'Sales Management',
    'sequence': 14,
    'summary': 'Sales, Product, Category, Clasification',
    'description': """
Sale Restrict Partners
======================
Users with group "Sale - Own Leads" can only see partners that are assigned to him or partners assigned to no one.
It also add actual user as default salesman for new partners
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'sale',
    ],
    'data': [
        'security/security.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: