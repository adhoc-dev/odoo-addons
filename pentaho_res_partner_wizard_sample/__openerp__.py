# -*- coding: utf-8 -*-
##############################################################################
#
#    Sistemas ADHOC - ADHOC SA
#    https://launchpad.net/~sistemas-adhoc
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
    'name': 'Pentaho res.partner report sample',
    'version': '1.0',
    'category': 'Reporting subsystems',
    'sequence': 14,
    'summary': '',
    'description': """
Titile of pentaho res.partner report sample
===========================================
This is a sample of a pentaho report using a custom wizard. 
The main modifications you should do are:
* report/res_partner.prpt --> your custom report
* report/report_data.xml --> everywhere you find the '<!-- MOD -->'' tag
* wizard/report_prompt.py --> everywhere you find the '# MOD' tag
* wizard/report_prompt.xml --> everywhere you find the '<!-- MOD -->'' tag
* Mod dependencies, name, description in this file
    """,
    'author':  'Sistemas ADHOC',
    'website': 'www.sistemasadhoc.com.ar',
    'images': [
    ],
    'depends': [
        'pentaho_reports',
    ],
    'data': [
        'wizard/report_prompt.xml',
        'report/report_data.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: