# -*- coding: utf-8 -*-
{
    "name": "Account Analytic / Contract Modifications",
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Quotations, Sales Orders, Invoicing',
    'description': """
Account Analytic / Contract Modifications
=========================================
* On creating invoice fill "reference" with contract name
* On creating invoice compute tax for total
* On creating invoice take only tax of contract company
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account_analytic_analysis',
    ],
    'data': [
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
