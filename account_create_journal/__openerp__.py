# -*- coding: utf-8 -*-

{
    "name": "Payment Journals Configuration",
    "version": "1.0",
    'author':  'Ingeniería ADHOC',
    'website': 'www.ingadhoc.com.ar',
    "category": "Accounting",
    "description": """ 
Configure And Create Payment Journals:
======================================
    """,
    'depends': [
		'account',
        'adhoc_base_setup',
        'account_payment_direction', 
        'account_check',
	],
    'data': [
        'wizard/journal_config_wizard_view.xml',
        'res_config_view.xml',
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
