# -*- coding: utf-8 -*-
{
    'name': 'Stock Picking EAN128 Report',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Stock Picking EAN128 Report
===========================

    """,
    'author':  'ADHOC',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'stock_ean128',
    ],
    'data': [
        'wizard/stock_print_remit_view.xml',
        'report/stock_report.xml'
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
