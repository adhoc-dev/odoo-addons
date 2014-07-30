# -*- coding: utf-8 -*-
{
    'name': 'Sale Mutiple Invoices by once',
    'version': '1.0',
    'category': 'Sales & Purchases',
    'sequence': 14,
    'summary': '',
    'description': """
Sale Mutiple Invoice
==================
On Invoicing from sale order, adds an option to make multiple invoices by once.
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'sale',
    ],
    'data': [
        'wizard/sale_make_invoice_advance.xml',
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