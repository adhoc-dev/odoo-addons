# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015, Eska Yazılım ve Danışmanlık A.Ş.
#    http://www.eskayazilim.com.tr
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
    'name': 'Journal Payment Method',
    'version': '1.0',
    'category': 'Account',
    'summary': 'Adds payment method field to cash and bank journals',
    'description': """
Journal Payment Method
====================================================

Adds payment method field to cash and bank journals.

This addon is used by addons that implement different payment methods such as check, credit card, promissory notes etc..
    """,
    'author': 'Eska Yazılım ve Danışmanlık A.Ş.',
    'website': 'http://www.eskayazilim.com.tr',
    'depends': ['account'],
    'data': ['views/account_journal_payment_method_view.xml'],
    'installable': True,
}


