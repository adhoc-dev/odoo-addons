# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Mentis d.o.o.
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

import time
from openerp.report import report_sxw

class account_interests(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_interests, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'parse_description': self._parse_description,
            'get_total_discount': self._get_total_discount,
            'get_total_net': self._get_total_net,
        })
        
    def _parse_description(self, desc, number):
        desc_list = desc.split(',')[number]
        word_list = desc_list.split(':')[1]
        return word_list.lstrip()
    
    def _get_total_discount(self, invoice):
        disc_total = 0
        for line in invoice.invoice_line:
            disc_total += line.quantity * line.price_unit * line.discount / 100
        return disc_total
    
    def _get_total_net(self, invoice):
        value_total = 0
        for line in invoice.invoice_line:
            value_total += line.quantity * line.price_unit
        return value_total
    
report_sxw.report_sxw('report.account.interests', 'account.invoice', 'account_interests/report/account_print_interests.rml', parser=account_interests)
