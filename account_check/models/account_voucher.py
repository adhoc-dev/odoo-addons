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

from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class account_voucher(osv.osv):

    _inherit = 'account.voucher'

    _columns = {
        'received_third_check_ids': fields.one2many('account.check','voucher_id', 'Third Checks', domain=[('type','=','third')], context={'default_type':'third','from_voucher':True}, required=False, readonly=True, states={'draft':[('readonly',False)]}),
        # 'issued_check_ids': fields.one2many('account.check','delivery_voucher_id', 'Issued Checks', required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'issued_check_ids': fields.one2many('account.check','voucher_id', 'Issued Checks', domain=[('type','=','issue')], context={'default_type':'issue','from_voucher':True}, required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'delivered_third_check_ids': fields.one2many('account.check','third_handed_voucher_id', 'Third Checks', domain=[('type','=','third')], context={'from_voucher':True}, required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'validate_only_checks': fields.related('journal_id','validate_only_checks',type='boolean', string='Validate only Checks', readonly=True,),
        'check_type': fields.related('journal_id','check_type',type='char', string='Check Type', readonly=True,),
        'issue_check_subtype': fields.related('journal_id','issue_check_subtype',type='char', string='Check subtype', readonly=True,),
        'amount_readonly': fields.related('amount', type='float', string='Total', digits_compute=dp.get_precision('Account'), readonly=True,),
    }
    
    _defaults = {
    }  

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'delivered_third_check_ids': False,
            'received_third_check_ids': False,
            'issued_check_ids': False,
        })
        return super(account_voucher, self).copy(cr, uid, id, default, context)
            
    def action_cancel_draft(self, cr, uid, ids, context=None):
        res =  super(account_voucher, self).action_cancel_draft(cr, uid, ids, context=None)
        check_domain = [('voucher_id','in',ids)]
        # check_domain = ['|',('voucher_id','in',ids),('third_handed_voucher_id','in',ids)]
        check_obj = self.pool['account.check']
        check_ids = check_obj.search(cr, uid, check_domain, context=context)
        check_obj.action_cancel_draft(cr, uid, check_ids)
        return res
        
    def cancel_voucher(self, cr, uid, ids, context=None):
        for voucher in self.browse(cr, uid, ids, context=context):
            for check in voucher.received_third_check_ids:
                if check.state not in ['draft','holding']:
                    raise osv.except_osv(_('Error!'), _('You can not cancel a voucher thas has received third checks in states other than "draft or "holding". First try to change check state.'))
            for check in voucher.issued_check_ids:
                if check.state not in ['draft','handed']:
                    raise osv.except_osv(_('Error!'), _('You can not cancel a voucher thas has issue checks in states other than "draft or "handed". First try to change check state.'))
            for check in voucher.delivered_third_check_ids:
                if check.state not in ['handed']:
                    raise osv.except_osv(_('Error!'), _('You can not cancel a voucher thas has delivered checks in states other than "handed". First try to change check state.'))
        res =  super(account_voucher, self).cancel_voucher(cr, uid, ids, context=None)
        check_domain = ['|',('voucher_id','in',ids),('third_handed_voucher_id','in',ids)]
        check_obj = self.pool['account.check']
        check_ids = check_obj.search(cr, uid, check_domain, context=context)
        for check in check_obj.browse(cr, uid, check_ids, context=context):
            check.signal_workflow('cancel')
        return res
        
    def proforma_voucher(self, cr, uid, ids, context=None):
        res =  super(account_voucher, self).proforma_voucher(cr, uid, ids, context=None)
        for voucher in self.browse(cr, uid, ids, context=context):
            if voucher.type == 'payment':
                for check in voucher.issued_check_ids:
                    check.signal_workflow('draft_router')
                for check in voucher.delivered_third_check_ids:
                    check.signal_workflow('holding_handed')                        
            elif voucher.type == 'receipt':
                for check in voucher.received_third_check_ids:
                    check.signal_workflow('draft_router')
        return res               

    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=None):        
        '''
        Override the onchange_journal function to check which are the page and fields that should be shown
        in the view.
        '''
        check_type = False
        validate_only_checks = False
        ret = super(account_voucher, self).onchange_journal(cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date, amount, ttype, company_id, context=context)
        if not ret:
            ret = {}
        if 'value' not in ret: ret['value'] = {}                
        if journal_id:        
            journal_obj = self.pool.get('account.journal')
            journal = journal_obj.browse(cr, uid, journal_id, context=context)
            if ids:
                for voucher in self.browse(cr, uid, ids, context=context):
                    if voucher.delivered_third_check_ids or voucher.received_third_check_ids or voucher.issued_check_ids:
                        # todo, este warning deberia sumarse a los warnings que pueden venir en ret['warning']
                        warning = {
                            'title': _('Check Error!'),
                            'message' : _('You can not change the journal if there are checks')
                        }
                        ret['warning']= warning
                        ret['value']['journal_id']= voucher.journal_id.id

                        # so that check_type is readed ok later
                        journal = voucher.journal_id
            else:
                ret['value']['delivered_third_check_ids'] = False
                ret['value']['received_third_check_ids'] = False
                ret['value']['issued_check_ids'] = False
            validate_only_checks = journal.validate_only_checks
            check_type = journal.check_type
        ret['value']['check_type'] = check_type
        ret['value']['validate_only_checks'] = validate_only_checks
        return ret

    def onchange_customer_checks(self, cr, uid, ids, received_third_check_ids, context=None):
        data = {}
        amount = self.get_one2many_amount(cr, uid, received_third_check_ids, context=context)
        data['amount'] = amount
        data['amount_readonly'] = amount
        return {'value': data}

    def onchange_supplier_checks(self, cr, uid, ids, delivered_third_check_ids, issued_check_ids, context=None):
        data = {}
        amount = 0.00
        third_checks = self.pool.get('account.check').browse(cr, uid, delivered_third_check_ids[0][2])
        for check in third_checks:
            amount += check.amount
        amount += self.get_one2many_amount(cr, uid, issued_check_ids, context=context)
        data['amount'] = amount
        data['amount_readonly'] = amount
        return {'value': data}

    def get_one2many_amount(self, cr, uid, check_ids, context=None):
        amount = 0.0
        for check in check_ids:
            check_amount = 0.0
            if check[0] == 0: # new check
                check_amount = check[2].get('amount', 0.00)
            elif check[0] == 1 and 'amount' in check[2]: # editing a check and amount being modified
                check_amount = check[2].get('amount', 0.00)
            elif check[0] == 4 or (check[0] == 1 and 'amount' not in check[2]): # already existing check
                check_id = check[1]
                check_amount = self.pool.get('account.check').browse(cr, uid, check_id, context).amount
            # elif check[0] == 2 --> se esta borrando, no lo tenemos en cuenta            
            amount += check_amount
        return amount
