# -*- coding: utf-8 -*-
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
                                              "Account Type's", required=True),
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
        active_ids = context.get('active_ids',False)

        # if no active_ids then called from menuitem
        if not active_ids:
            partner_id = self.pool['res.users'].browse(cr, uid, uid, context=context).partner_id.commercial_partner_id.id
            active_ids = [partner_id]
            context['active_ids'] = active_ids
            context['active_id'] = partner_id
            context['active_model'] = 'res.partner'
        return {'type' : 'ir.actions.report.xml',
                         'context' : context,
                         'report_name': 'report_account_summary'}
