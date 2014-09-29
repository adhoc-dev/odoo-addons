# -*- coding: utf-8 -*-


{
    'name': 'Clean Cancelled Invoice Number',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 14,
    'summary': 'Invoicing, Number, Cancelled',
    'description': """
Clean Cancelled Invoice Number
========================
Adds a button on invoice to allow clean number to cancelled invoices in order to:
* Regenerate the invoice number with new sequence number
* Delete the invoice
    """,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'depends': [
        'account_cancel'
    ],
    'data': [
        'account_invoice_view.xml',
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