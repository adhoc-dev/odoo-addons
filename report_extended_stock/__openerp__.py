# -*- coding: utf-8 -*-
{
    'name': 'Report Configurator - Stock',
    'version': '1.0',
    'category': 'Reporting Subsystem',
    'sequence': 14,
    'summary': '',
    'description': """
Report Configurator - Stock
=============================
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'report_extended',
        'stock',
    ],
    'data': [
        'views/report_view.xml',
        'views/stock_view.xml',
        'wizard/stock_transfer_details_view.xml',
        'report_extended_action_data.xml',
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
