# -*- encoding: utf-8 -*-
{
    "name": "Account Security Modifications",
    "version": "1.0",
    "description": """
Account Security Modifications
==============================
It makes the following modifications in security related to accounting:
-----------------------------------------------------------------------
* For group Invoicing & Payments: 
    * Allow to choose journals on invoices
    * Show move and unreconile ammount on vouchers lines 

    """,
    "author": "ADHOC SA",
    "website": "www.ingadhoc.com",
    "category": "Financial",
    "depends": [
        "account_voucher",
    ],
    "data": [
        'invoice_view.xml',
        'voucher_view.xml',
    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
