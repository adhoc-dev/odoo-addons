# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-Today OpenERP SA (<http://www.openerp.com>).
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
    'name': 'Web Support',
    'version': '1.0',
    'category': 'Web',
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar/',
    'description': '''This module present a more user friendly error message
window that give the user the possibility to send automatically an email
with the error information. The information include the debug information,
OpenERP instance that create it and the database name among other.

Also creates a Contract object that can be accessed in "Settings /
Publisher Warranty / Support Contract" for configuration. It should be configured
before it is possible to send email with the error information.

The information of the company that provides the support should be included in
the Support Contract entry as well.
''',
    'depends': ['web', 'mail', 'email_template'],
    'update_xml': [
        'support_contract_view.xml',
        'security/web_support_security.xml'],
    'js': ['static/src/js/web_support.js'],
    'qweb': ['static/src/xml/base.xml'],
    'css' : [ 'static/src/css/support.css', ],
    'installable': True,
}
