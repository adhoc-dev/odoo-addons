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
    'name':     'MRP auto production',
    'version':  '8.0.0.1.0',
    'author':   'ADHOC',
    'category': 'Localization/Argentina',
    'website':  'www.adhoc.com.ar',
    'license':  'AGPL-3',
    'description': """
Para probar instalar tambien "sale" y "procurement_jit_stock"
""",
    'depends': [
        'mrp',
        'procurement_jit_stock',
    ],
    'demo': [
        # TODO to fix data to pass test
        # 'mrp_demo.xml',
        ],
    'test': [],
    'data': [
        'mrp_view.xml',
    ],
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
