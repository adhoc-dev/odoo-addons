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
    'name': 'Journal Security',
    'version': '1.0',
    'category': '',
    'description': """
    Users can be assigned many Account Journals and then they can be
    restricted to see only this Journals.
    """,
    'author': 'ADHOC Sistemas',
    'website': 'http://www.adhocsistemas.com.ar/',
    'depends': ['account'],
    'init_xml': [],
    'update_xml': [
            'res_users_view.xml',
            'account_view.xml',
            'security/journal_security_security.xml'],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
}
