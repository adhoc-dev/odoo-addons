# -*- coding: utf-8 -*-
{
    "name": "Account Analytic Purchase Contract",
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Quotations, Sales Orders, Invoicing',
    'description': """
Account Analytic Purchase Contract
==================================
Manage Purchase Contracts and generate Recurring Invoices as you can do in
sales.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account_analytic_analysis',
        'purchase',
    ],
    'data': [
    'view/account_purchase_contract_view.xml',
    'view/account_purchase_contract_menu.xml',
    'account_analytic_analysis_cron.xml'
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
