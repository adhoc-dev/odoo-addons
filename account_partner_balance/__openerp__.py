# -*- coding: utf-8 -*-


{
    'name': 'Account Partner Balance',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': '',
    'description': """
Account Partner Balance
=======================

Adds a balance field on account.move.line. It also adds this field on account.move.line tree views
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account',
    ],
    'data': [
        'account_move_line_view.xml',
        'partner_view.xml',
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
