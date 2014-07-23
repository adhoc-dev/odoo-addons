# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: LIN Yu <lin.yu@elico-corp.com>
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
    'version': '1.0',
    'category': 'purchase',
    'sequence': 19,
    'description': """
Product Supplier Pricelist
==========================
Add sql constraint to restrict:
1. That you can only add one supplier to a product per company
2. That you can add olny one record of same quantity for a supplier pricelist

It also adds to more menus (and add some related fields) on purchase/product. 

    """,
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar',
    'images' : [],
    'depends': ['product',],
    'data': [
        'product_view.xml',
    ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: