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
    'name': 'Account Invoice Show Next Number',
    'version': '1.0',
    'category': 'Account',
    'description': """
Account Invoice Show Next Number
===================================================

Adds on customer draft invoices the next invoice number by the sequence.

TODO: make this optional on sale and sale_refund jornals
    """,
    'author': 'Sistemas ADHOC',
    'website': 'http://www.sistemasadhoc.com.ar',
    'depends': ['account'],
    'data': [
        'account_invoice_view.xml',
#        'account_journal_view.xml',
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
