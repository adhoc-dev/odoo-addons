# -*- coding: utf-8 -*-
##############################################################################
#
#    Logistic
#    Copyright (C) 2014 No author.
#    No email
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


{   'active': False,
    'author': 'Sistemas ADHOC.',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [
        'purchase_double_validation',
        ],
    'description': u"""
Purchase double validation improovements
========================================
Adds a button for confirmed orders so that you can print the purchase order. 
""",
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Purchase Double Validation Improovements',
    'test': [],
    'update_xml': [
        'view/purchase_view.xml',
      ],
    'version': 'No version',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
