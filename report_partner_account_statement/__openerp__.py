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
    'name': 'Report Partner Account Statement',
    'version': '1.0',
    'description': """Report Partner Account Statement""",
    'category': 'Aeroo Reporting',
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar/',
    'depends': ['sale', 'report_aeroo', 'report_aeroo_ooo'],
    'init_xml': [],
    'update_xml': [
        'wizard/account_summary_wizard_view.xml',
        'report/account_summary_report.xml',],
    'demo_xml': [],
    'test':[],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
