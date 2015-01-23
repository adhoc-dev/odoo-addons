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
        # we add sale depency because invoice report inheritance error, it also
        # make sense because this module is only usefull if sale is installed
        'sale',
    ],
    'data': [
        'report/invoice_report_view.xml',
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
