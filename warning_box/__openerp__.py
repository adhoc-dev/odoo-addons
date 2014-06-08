# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Warning box",
    'version': '0.1',
    'category': 'Tools',
    'description': """
        [ENG] Add Warning box.
        usage return self.pool.get('warning_box').info(cr, uid, title='The title', message='the message')   
    """,
    'author': 'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'license': 'AGPL-3',
    "depends": ['base'],
    "data": ['warning_box.xml',
             ],
    "active": False,
    "installable": True
}
