# -*- coding: utf-8 -*-
{
    "name": "Partner Samples",
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Quotations, Sales Orders, Invoicing',
    'description': """
Partner Samples
===============
Add information about samples given to partners
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'product',
    ],
    'data': [
        'partner_view.xml',
        'partner_sample_view.xml',
        'security/partner_sample_security.xml',
        'security/ir.model.access.csv',
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
