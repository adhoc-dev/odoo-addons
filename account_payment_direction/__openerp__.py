# -*- coding: utf-8 -*-
{'active': False,
    'author': 'Ingenieria ADHOC',
    'category': 'Accounting & Finance',
    'demo_xml': [],
    'depends': ['account_voucher'],
    'description': '''
Account Payment Direction
=========================
Extends Account Journal and adds a field direction (in or out) for bank and cash Journals. 
This journals will be shown or not on customer or supplier vouchers depending on the 'in', 'out' config. 
Specially used for journals that are only used on payments (like retentions)
''',
    'init_xml': [],
    'installable': True,
    'name': 'Account Payment Direction',
    'test': [],
    'update_xml': [
        'account_journal_view.xml',
        'voucher_payment_receipt_view.xml',
    ],
    'version': '0.0',
    'website': 'www.ingadhoc.com'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
