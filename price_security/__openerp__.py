# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Price Security',
    'version': '8.0.2.1.1',
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
    'author': 'ADHOC SA',
    'website': 'http://www.adhoc.com.ar/',
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
