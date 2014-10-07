# -*- coding: utf-8 -*-
{
    'name': 'Report Configurator - Voucher Receipt',
    'version': '1.0',
    'category': 'Reporting Subsystem',
    'sequence': 14,
    'summary': '',
    'description': """
Report Configurator - Account
=============================
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'report_extended',
        'account_voucher_receipt',
        'account_check',
    ],
    'data': [
        'views/report_view.xml',
        'views/account_voucher_receipt_view.xml',
        'views/account_action_data.xml',
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
