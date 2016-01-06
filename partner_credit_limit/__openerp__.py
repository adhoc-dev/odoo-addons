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
    'name': 'Partner Credit Limit',
    'version': '8.0.1.1.0',
    'description': """Partner Credit Limit
    When approving a Sale Order it computes the sum of:
        * The credit the Partner has to paid
        * The amount of Sale Orders aproved but not yet invoiced
        * The invoices that are in draft state
        * The amount of the Sale Order to be aproved
    and compares it with the credit limit of the partner. If the
    credit limit is less it does not allow to approve the Sale
    Order""",
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'depends': ['sale'],
    'data': [
        'security/partner_credit_limit_security.xml',
        'partner_view.xml',
        ],
    'demo': ['partner_demo.xml'],
    'test': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
