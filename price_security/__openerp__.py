# -*- coding: utf-8 -*-
{
    'name': 'Price Security',
    'version': '2.0',
    'description': """
Price Security
==============
Creates a new permission to restrict the users that can modify the prices
of the products.

Asociate to each user a list of pricelist and the correspoding discounts they
can apply to sale orders and invoices.

Allow the posibility to mark products so that anyone can modify their price in
a sale order.
""",
    'category': 'Sales Management',
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar/',
    'depends': [
        'sale',
    ],
    'data': [
        'views/res_users_view.xml',
        'views/sale_view.xml',
        'views/invoice_view.xml',
        'views/product_view.xml',
        'security/ir.model.access.csv',
        ],
    'demo_xml': [],
    'test': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
