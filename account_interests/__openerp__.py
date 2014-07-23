# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Mentis d.o.o. (<http://www.mentis.si>)
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
    "name": "Calculate interests for selected partners",
    "version": "1.0",
    'author': u'Sistemas ADHOC',
    "category": "Accounting",
    'website': 'www.sistemasadhoc.com.ar',
    "depends": ['l10n_ar_debit_note',],
    "description": """Calculate interests for selected partners.""",
    "init_xml": [],
    "update_xml": [
		# 'interests_report.xml',
	    # 'wizard/account_interests_view.xml',
        'interest_view.xml',
        'security/ir.model.access.csv',
    ],
    "demo_xml": [],
    "active": False,
    "installable": True,
}
