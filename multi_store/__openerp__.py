# -*- coding: utf-8 -*-
{
    'name': 'Multi Store',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': '',
    'description': """
Multi Store
===========
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account',
    ],
    'data': [
            'res_users_view.xml',
            # 'account_view.xml',
            # 'security/journal_security_security.xml',
            'security/multi_store_security.xml',
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