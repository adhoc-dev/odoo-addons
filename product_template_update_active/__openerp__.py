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
    'author': 'ADHOC SA.',
    'category': 'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': ['product'],
    'description': """
Product Template Update Active Field
====================================

Update active field of product template in this way:
* If any related product product to this template has active = True, set True
* If all related product product to this template has active = False, set False
""",
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Product Template Update Active Field',
    'test': [],
    'data': [
        'wizard/product_template_update_active_field_view.xml',
    ],
    'website': 'www.adhoc.com.ar'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
