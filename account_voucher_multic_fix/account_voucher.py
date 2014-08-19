# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import api
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import netsvc

class account_voucher(osv.osv):

    _inherit = "account.voucher"
    _columns = {
        }

    _defaults = {
    }
        
    def on_change_company(self, cr, uid, ids, date, currency_id, payment_rate_currency_id, amount, company_id, context=None):
        ''' We add this function so that journal_id value and domain is updated when 
        company_id is change. We also call to onchange_date in order to update the 
        selected period'''

        # Run onchange_date to update period and other values
        result = self.onchange_date(cr, uid, ids, date, currency_id, payment_rate_currency_id, amount, company_id, context=context)
        if 'domain' not in result: result['domain'] = {} 
        if 'value' not in result: result['value'] = {} 

        journal_id = False
        journal_ids = []
        if company_id:
            journal_ids = self.pool['account.journal'].search(cr, uid, [('company_id','=',company_id),
                ('type','in',('cash', 'bank'))], context=context)
            if journal_ids:                
                journal_id = journal_ids[0]
        journal_domain = [('id','in',journal_ids)]
        result['domain']['journal_id'] = journal_domain
        result['value']['journal_id'] = journal_id
        return result

    # TODO borrar esto si no lo usamos. Dejamos estas funciones porque es probable que alguna tengamos que modificar
    # def _get_period(self, cr, uid, context=None):
    #     print 'context', context
    #     if context is None: context = {}
    #     if context.get('period_id', False):
    #         return context.get('period_id')
    #     periods = self.pool.get('account.period').find(cr, uid, context=context)
    #     print 'periods and periods[0] or False', periods and periods[0] or False
    #     return periods and periods[0] or False

    # def _get_journal(self, cr, uid, context=None):
    #     if context is None: context = {}
    #     invoice_pool = self.pool.get('account.invoice')
    #     journal_pool = self.pool.get('account.journal')
    #     if context.get('invoice_id', False):
    #         currency_id = invoice_pool.browse(cr, uid, context['invoice_id'], context=context).currency_id.id
    #         journal_id = journal_pool.search(cr, uid, [('currency', '=', currency_id)], limit=1)
    #         return journal_id and journal_id[0] or False
    #     if context.get('journal_id', False):
    #         return context.get('journal_id')
    #     if not context.get('journal_id', False) and context.get('search_default_journal_id', False):
    #         return context.get('search_default_journal_id')

    #     ttype = context.get('type', 'bank')
    #     if ttype in ('payment', 'receipt'):
    #         ttype = 'bank'
    #     res = self._make_journal_search(cr, uid, ttype, context=context)
    #     return res and res[0] or False

    # def _make_journal_search(self, cr, uid, ttype, context=None):
    #     if not context:
    #         context = {}
    #     print 'context', context
    #     company_id = context.get('company_id', False)
    #     print 'company_id', company_id
    #     journal_pool = self.pool.get('account.journal')
    #     domain = [('type', '=', ttype)]
    #     if company_id:
    #         domain.append(('company_id','=',company_id))
    #     return journal_pool.search(cr, uid, domain, limit=1)

    def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
        '''Modification of this method so that only the moves of selected journal company are
        considered'''

        if not context:
            context = {}
        move_line_pool = self.pool.get('account.move.line')
        journal_pool = self.pool.get('account.journal')
        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        account_type = None
        if context.get('account_id'):
            account_type = self.pool['account.account'].browse(cr, uid, context['account_id'], context=context).type
        if ttype == 'payment':
            if not account_type:
                account_type = 'payable'
        else:
            if not account_type:
                account_type = 'receivable'        
        move_line_ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('company_id','=',journal.company_id.id), ('account_id.type', '=', account_type), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
        if move_line_ids:
            context['move_line_ids'] = move_line_ids
        else:            
            return {
                'value': {'line_dr_ids': [] ,'line_cr_ids': [] ,'pre_line': False,},
            }        
        return super(account_voucher, self).recompute_voucher_lines(cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=context)