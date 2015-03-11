# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{'active': False,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'category': 'Accounting & Finance',
    'data': [
        'security/account_voucher_receipt_security.xml',
        'security/ir.model.access.csv',
        'views/account_voucher_view.xml',
        'views/account_voucher_receipt_view.xml',
        'views/account_voucher_receiptbook_view.xml',
        'views/res_config_view.xml',
        'workflow/account_voucher_receipt_workflow.xml',
        'data/receipt_data.xml',
    ],
    'demo': [],
    'depends': ['account_voucher'],
    'description': '''
Receipt
=======

* See if invoice, in the payment tab , we show more the vouachers than notes
* That can only confirm receipt if all vouchers associated are validated
* Add in another module report receipt and buttons
''',
    'installable': True,
    'name': 'Voucher Receipts',
    'test': [],
    'version': '1.243'}
