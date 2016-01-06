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
    'name': 'Stock availability in sales order line',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'description': """
Stock availability in sales order line
======================================
* Add two groups. One for seeing stock on sale orders and other to see only if or not available
* Add an option in warehouse to disable stock warning

IMPORTANT:
----------
    * This module could break some warnings as the ones implemented by "warning" module
    * If you dont disable warning and give a user availbility to see only "true/false" on sale order stock, he can see stock if the warning is raised
    """,
    'author': 'Moldeo Interactive & ADHOC SA',
    'website': 'http://business.moldeo.coop http://adhoc.com.ar/',
    'license': 'AGPL-3',
    'images': [],
    'depends': [
        'sale_stock'
    ],
    'demo': [],
    'data': [
        'sale_view.xml',
        'stock_view.xml',
        'security/sale_order.xml',
        ],
    'test': [],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
