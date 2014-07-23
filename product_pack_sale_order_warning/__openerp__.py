# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Product Pack Sale Order Warning',
    'version': '1.0',
    'category': 'Base',
    'description': """When installing the module nan_product_pack, when a pack product
that is stock dependant is defined, if the components of the pack products are out of
stock no warning is shown when selecting the pack product.

This module make the warning appears when necessary.""",
    'author': 'ADHOC Sistemas',
    'website': 'http://www.adhocsistemas.com.ar/',
    'depends': ['nan_product_pack'],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
