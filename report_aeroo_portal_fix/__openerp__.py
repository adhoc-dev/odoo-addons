# -*- coding: utf-8 -*-
{
    'name': 'Report Aeroo Portal Fix',
    'version': '1.0',
    'category': '',
    'sequence': 14,
    'summary': '',
    'description': """
Report Aeroo Portal Fix
=======================
Give access to output mime types
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'report_aeroo',
        'portal',
    ],
    'data': [
        'security/ir.model.access.csv',
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