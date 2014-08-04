# -*- coding: utf-8 -*-
{
    "name": "Account Journal Sequence",
    "version": "1.0",
    'author':  'Ingeniería ADHOC',
    'website': 'www.ingadhoc.com.ar',
    "category": "Accounting",
    "description": """ 
Account Journal Sequence
========================
Adds sequence field on account journal and it is going to be considered when choosing journals in differents models.
    """,
    'depends': [
		'account',
	],
    'data': [
        'account_journal_view.xml',
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
