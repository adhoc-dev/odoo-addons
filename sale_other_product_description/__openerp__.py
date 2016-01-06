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
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'category': 'Accounting & Finance',
    'data': [
        'product_view.xml',
        'report.xml',
    ],
    'demo': [],
    'depends': [
        'l10n_ar_aeroo_invoice',
        'l10n_ar_aeroo_stock',
        'l10n_ar_aeroo_einvoice',
        ],
    'description': '''
Sale Other Product Description
==============================
Add "Other Sale Description" field on Products. If this field is set,
then on sale orders lines this description will be used and no code.
''',
    'installable': True,
    'name': 'Sale Other Product Description',
    'test': [],
    'version': '8.0.1.2.0'}
