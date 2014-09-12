# -*- coding: utf-8 -*-
{
    "name": "Calculate interests for selected partners",
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Quotations, Sales Orders, Invoicing',
    'description': """
Interests Management
====================
HACER APP, poner icono y dejar pendiente descripcion a cuando juan lo termine
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'l10n_ar_invoice',
    ],
    'data': [
        'interest_view.xml',
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