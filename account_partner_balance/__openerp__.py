# -*- coding: utf-8 -*-
##############################################################################
#
#    
#    Copyright (C) 2013 Agrihold - Adhoc - Moldeo.
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
    'author': 'Sistemas ADHOC',
    'category': 'Accounting & Finance',
    'demo_xml': [
    ],
    'depends': ['account'],
    'description': 'Adds a balance field on account.move.line. It also adds this field on account.move.line tree views',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Account Partner Balance',
    'test': [],
    'update_xml': [
        'account_move_line_view.xml',
        'partner_view.xml',
        ],
    'version': 'No version',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
