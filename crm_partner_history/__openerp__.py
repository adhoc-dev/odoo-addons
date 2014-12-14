# -*- coding: utf-8 -*-
{
    'name': 'CRM Partner History',
    'version': '1.0',
    'category': 'Sales & Purchases',
    'sequence': 14,
    'summary': '',
    'description': """
CRM Partner History
===================
Adds CRM partner history page on partners form view as it exists on odoo v6.1
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'crm',
    ],
    'data': [
        'partner_view.xml',
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
