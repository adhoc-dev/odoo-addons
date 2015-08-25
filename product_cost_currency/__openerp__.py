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
    "name": "Product Cost Currency",
    'version': '8.0.1.0.0',
    'category': 'Product',
    'sequence': 14,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': 'Allow to define purchase prices on different currencies using\
 replenishment cost field',
    "description": """
Product Cost Currency
=====================
Allows to define product cost in differents currencies

Repository dependencies
-----------------------
Requires repository: https://github.com/OCA/margin-analysis

How to use?
-----------
1. Install
2. Configure pricelist to use new price_type "Replanishment Cost"
3. Use the new fields on product "procuerements" tab
    """,
    "depends": [
        "product_replenishment_cost",
    ],
    'external_dependencies': {
    },
    "data": [
        'views/product_view.xml',
        'data/price_type_data.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    "installable": True,
    'auto_install': False,
    'application': False,
}
