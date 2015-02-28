# -*- coding: utf-8 -*-
{
    'author': 'Ingenieria ADHOC',
    'auto_install': False,
    'installable': True,
    'category': 'Tools',
    'demo_xml': [
    ],
    'depends': [
        'base',
        'mail'
    ],
    'description': """
Partners User
=============
Add partner user related fields on partner and add them in partner view. Also adds an action that allow quick creation of user. 
For using the quick creation you must set a "template user" for the partner, you can do it by context or making this field visible. 
    """,
    'init_xml': [],
    'license': 'AGPL-3',
    'name': u'Partner User',
    'test': [],
    'data': [
        'partner_view.xml',
        'security/ir.model.access.csv',
    ],
    'version': '1.1',
    'website': 'www.ingadhoc.com',
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
