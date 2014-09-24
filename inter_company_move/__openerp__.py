# -*- coding: utf-8 -*-
{
    'name': 'Inter Company Move',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Moves documents around companies in a multicompany environment,',
    'description': """
Inter Company Move
==================
    """,
    'author':  'ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account',
    ],
    'data': [
        'views/res_company_view.xml',
        'views/account_invoice_view.xml',
        'wizard/inter_company_move_wizard_view.xml',
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