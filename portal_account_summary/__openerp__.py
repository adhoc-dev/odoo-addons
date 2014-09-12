# -*- coding: utf-8 -*-
{
    'name': 'Portal Account Summary',
    'version': '1.0',
    'category': '',
    'sequence': 14,
    'summary': '',
    'description': """
Portal Account Summary
======================
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account_partner_account_summary',
        'portal',
        'report_aeroo_portal_fix',
        'portal_partner_fix',
    ],
    'data': [
        'account_summary_view.xml',
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