# -*- coding: utf-8 -*-


{
    'name': 'Payable vs Receivable Adjustments',
    'version': '1.0',
    'category': 'account_voucher.pyc',
    'summary' : 'Adjust Payable vs Receivable Accounts',
    'description': """
Adjust Customer and Suppliers Invoices
=========================================
This module helps you to adjust Customer and Suppliers Invoices from the same party. You can reconcile customer and suppliers account against each other.

How it works?
+++++++++++++++++
When a company or contact is supplier as well as customer, you can adjust payments of your customer and supplier invoices from this same company or contact.

**Example:**

* Agrolait, Customer Invoice for Sales = $1000
* Agrolait, Supplier Invoice for Purchases = $900

Create Customer Payment and select Agrolait as customer and the system will automatically adjust $1000 Credit with $900 Debit entries. So you can collect only $100 from Agrolait. Both the invoices will be paid once you reconcile the entries.

Video Tutorial: http://www.youtube.com/watch?v=2Zeg0WYJcbg
""",
    'author': 'OpenERP SA',
    'website': 'http://www.openerp.com',
    'images': [],
    'depends': ['account_voucher'],
    'data': [
        
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
