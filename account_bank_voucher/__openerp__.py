# -*- encoding: utf-8 -*-
{
    "name": "Bank and Cash Statement with Vouchers",
    "version": "1.0",
    "description": """
Manage the bank/cash reconciliation with account vouchers (payments and receipts)
=================================================================================

The management of treasury require integrate the payments of customers and suppliers to bank statements, allowing real bank reconciliations.

Key Features
------------
* Add button on bank statement to add vouchers
* Integrate the account vouchers with the bank statements
* Optimize the payments and receipts in treasury management
* Fix some features on bank statements to enable the bank reconciliation

    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Financial",
    "depends": [
        "account",
        "account_voucher",
    ],
    "data": [
        "wizard/bank_statement_populate_view.xml",
        "account_view.xml",
    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
