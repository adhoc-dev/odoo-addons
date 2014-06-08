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

import netsvc

from osv import fields, osv
import pooler

class account_summary_wizard(osv.osv_memory):
    _name = 'account_summary_wizard'
    _description = 'account_summary_wizard'
    
    _columns = {
        'from_date': fields.date('From'),
        'to_date': fields.date('To'),
        'show_invoice_detail': fields.boolean('Show Invoice Detail'),
        'show_receipt_detail': fields.boolean('Show Receipt Detail'),
        'result_selection': fields.selection([('customer','Receivable Accounts'),
                                              ('supplier','Payable Accounts'),
                                              ('customer_supplier','Receivable and Payable Accounts')],
                                              "Partner's", required=True),
    }
    
    _defaults = {
        'result_selection': 'customer_supplier',
    }
    
    def account_summary(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids, context=context)[0]
        
        from_date = False
        to_date = False
        show_invoice_detail = False
        show_receipt_detail = False
        result_selection = False
        
        if wizard.from_date:
            from_date = wizard.from_date
        if wizard.to_date:
            to_date = wizard.to_date
        if wizard.show_invoice_detail:
            show_invoice_detail = wizard.show_invoice_detail
        if wizard.show_receipt_detail:
            show_receipt_detail = wizard.show_receipt_detail
        if wizard.result_selection:
            result_selection = wizard.result_selection
        
        if not context:
            context = {}
        context['from_date'] = from_date
        context['to_date'] = to_date
        context['show_invoice_detail'] = show_invoice_detail
        context['show_receipt_detail'] = show_receipt_detail
        context['result_selection'] = result_selection
        
        return {'type' : 'ir.actions.report.xml',
                         'context' : context,
                         'report_name': 'report_account_summary'}
    
account_summary_wizard()










