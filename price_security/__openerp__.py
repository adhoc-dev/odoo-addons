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

For users with price restriction, it restricts:
* on sales orders: change payment term or pricelist
* on sales order lines: change unit price and set limits on discount (limits configured on user)
* on partners: change payment term or pricelist
* on invoices: change unit price
* on product: change price

""",
    'category': 'Sales Management',
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar/',
    'depends': [
        'sale',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_users_view.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/invoice_view.xml',
        'views/partner_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
