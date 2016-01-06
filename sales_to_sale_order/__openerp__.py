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
    'name': 'Sales to Sale Order',
    'version': '8.0.1.0.0',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends' : ["sale"],
    'category' : 'Sale Management',
    'description': '''
Sales to Sale Order
===================
This module create a wizard asociated to an action on Sale
Orders. This wizard generates a Sale Order in another company for all sale orders items.
    ''',
    'demo' : [
        'portal_demo.xml',
    ],
    'data' : [
        'security/sales_t_sale_order_security.xml',
        'wizard/sales_to_sale_order_wizard_view.xml',
        'res_users_view.xml',
        'sale_view.xml',
        ],
    'installable': True
}
