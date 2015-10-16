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
    "name": "Sale Exceptions Ingore Approve Directly",
    'version': '8.0.1.0.0',
    'category': 'Product',
    'sequence': 14,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': 'Allow to define purchase prices on different currencies using\
 replenishment cost field',
    "description": """
Sale Exceptions Ingore Approve Directly
=======================================
When Ignoring a sale Exception, approve directly the sale order
    """,
    "depends": [
        "sale_exceptions",
    ],
    'external_dependencies': {
    },
    "data": [
        'wizard/sale_exception_confirm_view.xml',
        'views/sale_view.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    "installable": True,
    'auto_install': False,
    'application': False,
}
