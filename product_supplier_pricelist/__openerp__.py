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
    'name': 'Product Supplier Pricelist',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'sequence': 14,
    'summary': '',
    'description': """
Product Supplier Pricelist
==========================
Add sql constraint to restrict:
1. That you can only add one supplier to a product per company
2. That you can add olny one record of same quantity for a supplier pricelist

It also adds to more menus (and add some related fields) on purchase/product. 
    """,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'purchase',
    ],
    'data': [
        'product_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    # TODO fix this module and make installable
    'installable': False,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: