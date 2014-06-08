# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
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

from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
import logging
_logger = logging.getLogger(__name__)

class account_check(osv.osv):

    _name = 'account.check'
    _description = 'Account Check'
    _order = "id desc"
    _inherit = ['mail.thread']    

    def _get_name(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=None):
            if line.checkbook_id:
                padding = line.checkbook_id.padding
            else:
                # TODO make padding configurable
                padding = 8        
            res[line.id] = '%%0%sd' % padding % line.number
        return res

    def _get_destiny_partner(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=None):
            partner_id = False
            if line.type == 'third' and line.third_handed_voucher_id:
                partner_id = line.third_handed_voucher_id.partner_id.id
            elif line.type == 'issue':
                partner_id = line.voucher_id.partner_id.id
            res[line.id] = partner_id
        return res

    def _get_source_partner(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=None):
            partner_id = False
            if line.type == 'third':
                partner_id = line.voucher_id.partner_id.id
            res[line.id] = partner_id
        return res

    _columns = {
        'name': fields.function(_get_name, type='char', string='Number',),
        'number': fields.integer('Number', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'amount': fields.float('Amount', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'voucher_id': fields.many2one('account.voucher', 'Voucher', readonly=True, required=True),
        'type': fields.related('voucher_id', 'journal_id', 'check_type', type='selection', selection=[('issue', 'Issue'),('third', 'Third')], string='Type', required=True, readonly=True, store=True),
        'journal_id': fields.related('voucher_id', 'journal_id', type='many2one', relation="account.journal", string='Journal', readonly=True, store=True),
        'issue_date': fields.date('Issue Date', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'payment_date': fields.date('Payment Date', readonly=True, help="Only if this check is post dated", states={'draft': [('readonly', False)]}),
        'destiny_partner_id': fields.function(_get_destiny_partner, relation='res.partner', type="many2one", string='Destiny Partner',),
        'user_id' : fields.many2one('res.users', 'User', readonly=True),  
        'clearing': fields.selection((
                ('24', '24 hs'),
                ('48', '48 hs'),
                ('72', '72 hs'),
            ), 'Clearing',readonly=True,states={'draft': [('readonly', False)]}),
        'state': fields.selection((
                ('draft', 'Draft'),
                ('holding', 'Holding'),
                ('deposited', 'Deposited'),
                ('handed', 'Handed'),
                ('rejected', 'Rejected'),
                ('debited', 'Debited'),
                ('cancel', 'Cancel'),
            ), 'State', required=True, track_visibility='onchange'),        
        'supplier_reject_debit_note_id':fields.many2one('account.invoice','Supplier Reject Debit Note', readonly=True,),
        'expense_account_move_id': fields.many2one('account.move','Expense Account Move', readonly=True),

        # Related fields
        'company_id': fields.related('voucher_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),

        # Issue Check
        'issue_check_subtype': fields.related('checkbook_id', 'issue_check_subtype', type='char', string='Subtype', readonly=True, store=True),
        'checkbook_id': fields.many2one('account.checkbook', 'Checkbook', readonly=True, states={'draft': [('readonly', False)]}),
        'debit_account_move_id': fields.many2one('account.move','Debit Account Move', readonly=True),

        # Third check 
        'third_handed_voucher_id': fields.many2one('account.voucher', 'Handed Voucher', readonly=True,),       
        'source_partner_id': fields.function(_get_source_partner, relation='res.partner', type="many2one", string='Source Partner',),
        'customer_reject_debit_note_id': fields.many2one('account.invoice','Customer Reject Debit Note', readonly=True,),
        'bank_id': fields.many2one('res.bank', 'Bank', readonly=True, states={'draft': [('readonly', False)]}),
        'vat': fields.char('Vat', size=11, states={'draft': [('readonly', False)]}),
        'deposit_account_move_id': fields.many2one('account.move','Deposit Account Move', readonly=True),
        # this one is used for check rejection
        'deposit_account_id': fields.many2one('account.account','Deposit Account', readonly=True),
    }

    def _check_number_interval(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.type !='issue' or (obj.checkbook_id and obj.checkbook_id.range_from <= obj.number <= obj.checkbook_id.range_to):
                return True
        return False

    def _check_number_issue(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.type =='issue':
                same_number_check_ids = self.search(cr, uid, [('id','!=',obj.id),('number','=',obj.number),('checkbook_id','=',obj.checkbook_id.id)], context=context)
                if same_number_check_ids:
                    return False
        return True

    def _check_number_third(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.type =='third':
                same_number_check_ids = self.search(cr, uid, [('id','!=',obj.id),('number','=',obj.number),('voucher_id.partner_id','=',obj.voucher_id.partner_id.id)], context=context)
                if same_number_check_ids:
                    return False
        return True

    _constraints = [
        (_check_number_interval, 'Check Number Must be in Checkbook interval!', ['number','checkbook_id']),
        (_check_number_issue, 'Check Number must be unique per Checkbook!', ['number','checkbook_id']),
        (_check_number_third, 'Check Number must be unique per Customer and Bank!', ['number','bank_id']),
    ]

    def _get_checkbook_id(self, cr, uid, context=None):
        res={}
        if context is None: 
            context = {}
        journal_id = context.get('default_journal_id', False)
        check_type = context.get('default_type',False)
        if journal_id and check_type == 'issue':
            checkbook_pool = self.pool.get('account.checkbook')
            res = checkbook_pool.search(cr, uid, [('state', '=', 'active'),('journal_id', '=', journal_id)],)            
            if res:
                return res[0] 
        else:
            return False    

    _defaults = {
        'state': 'draft',
        'issue_date': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda s, cr, u, c: u,
        'checkbook_id': _get_checkbook_id, 
    }    
  
    def onchange_date(self, cr, uid, ids, issue_date, payment_date, context=None):
        res = {}
        if issue_date and payment_date and issue_date > payment_date:
            res = {'value':{'payment_date': False}}
            res.update({'warning': {'title': _('Error !'), 'message': _('Payment Date must be greater than Issue Date')}})
        return res
        
    def onchange_vat(self, cr, uid, ids, vat, context=None):
        res = {}
        if not vat:
            res.update({'warning': {'title': _('Error !'), 'message': _('Vat number must be not null !')}})
        else:
            if len(vat) != 11:
                res = {'value':{'vat': None}}
                res.update({'warning': {'title': _('Error !'), 'message': _('Vat number must be 11 numbers !')}})
            else:    
                res = {'value':{'vat': vat}}
        return res    
        
    def unlink(self, cr, uid, ids, context=None):
        for record in self.browse(cr,uid,ids,context=context):
            if  record.state not in ('draft'):
                raise osv.except_osv(_('Error !'), _('The Check must be in draft state for unlink !'))
                return False 
        return super(account_check, self).unlink(cr, uid, ids, context=context)     

    def onchange_checkbook_id(self, cr, uid, ids, checkbook_id, context=None):
        values = {}
        checkbook_obj = self.pool.get('account.checkbook')
        number = False
        issue_check_subtype = False
        if checkbook_id:
            checkbook = checkbook_obj.browse(cr, uid, checkbook_id, context=context)
            number = checkbook.next_check_number
            issue_check_subtype = checkbook.issue_check_subtype
        values = {
            'number': number,
            'issue_check_subtype': issue_check_subtype,
            }
        return {'value':values}     

    def action_cancel_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        self.delete_workflow(cr, uid, ids)
        self.create_workflow(cr, uid, ids)        

    def action_hold(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            check.write({
                'state': 'holding',
                 })
        return True

    def action_deposit(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            check.write({
                'state': 'deposited',
                 })
        return True

    def action_hand(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            check.write({
                'state': 'handed',
                 })
        return True

    def action_reject(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            check.write({
                'state': 'rejected',
                 })
        return True

    def action_debit(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            check.write({
                'state': 'debited',
                 })
        return True

    def action_cancel_rejection(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            if check.customer_reject_debit_note_id:
                raise osv.except_osv(_('Error !'), _('To cancel a rejection you must first delete the customer reject debit note!'))
            if check.supplier_reject_debit_note_id:
                raise osv.except_osv(_('Error !'), _('To cancel a rejection you must first delete the supplier reject debit note!'))
            if check.expense_account_move_id:
                raise osv.except_osv(_('Error !'), _('To cancel a rejection you must first delete Expense Account Move!'))
            print 'check', check
            check.signal_workflow('cancel_rejection')
        return True

    def action_cancel_debit(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            if check.debit_account_move_id:
                raise osv.except_osv(_('Error !'), _('To cancel a debit you must first delete Debit Account Move!'))
            check.signal_workflow('debited_handed')
        return True

    def action_cancel_deposit(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            if check.deposit_account_move_id:
                raise osv.except_osv(_('Error !'), _('To cancel a deposit you must first delete the Deposit Account Move!'))
            check.signal_workflow('cancel_deposit')
        return True
        
    def action_cancel(self, cr, user, ids, context=None):
        for check in self.browse(cr, user, ids):
            check.write({
                'state': 'cancel',})
        return True

