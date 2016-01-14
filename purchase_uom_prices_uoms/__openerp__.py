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
    'name': 'Purchase UOM Prices',
    'version': '8.0.0.0.1',
    'category': 'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [
        'purchase',
        'product_uom_prices',
    ],
    'description': """
Purchase UOM Prices
==================
* Add a o2m field on products to allow defining prices in different uoms
* Add a new type of price calculation on pricelists (for the new o2m field
    on products)
* Change domain on purchase order lines so that only defined uoms can be choosen.

""",
    'author': 'ADHOC SA.',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'test': [],
    'data': [
    ],
    'installable': True}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
