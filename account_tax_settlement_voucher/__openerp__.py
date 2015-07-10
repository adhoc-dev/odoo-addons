# -*- coding: utf-8 -*-
{
    'name': 'Tax Settlement - Voucher Integration',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': '',
    'description': """
Tax Settlement - Voucher Integration
====================================
Add pay button on tax settlement
Add settlement moves on voucher
    """,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'account_tax_settlement',
        'account_voucher',
    ],
    'data': [
        'views/account_voucher_pay_settlement.xml',
        'views/account_voucher_view.xml',
        'views/account_move_line_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
