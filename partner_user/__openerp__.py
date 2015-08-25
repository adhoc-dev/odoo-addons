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
    'author': 'ADHOC SA',
    'auto_install': False,
    'installable': True,
    'category': 'Tools',
    'demo_xml': [
    ],
    'depends': [
        'base',
        'mail'
    ],
    'description': """
Partners User
=============
Add partner user related fields on partner and add them in partner view. Also adds an action that allow quick creation of user. 
For using the quick creation you must set a "template user" for the partner, you can do it by context or making this field visible. 
    """,
    'license': 'AGPL-3',
    'name': u'Partner User',
    'test': [],
    'data': [
        'partner_view.xml',
        'security/ir.model.access.csv',
    ],
    'version': '8.0.1.1.0',
    'website': 'www.adhoc.com.ar',
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
