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
import logging
_logger = logging.getLogger(__name__)

class account_checkbook(osv.osv):
    
    _name = 'account.checkbook'
    _description = 'Account Checkbook'
    _inherit = ['mail.thread']


    def _get_next_check_number(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        for checkbook in self.browse(cr, uid, ids, context=None):
            next_number = checkbook.range_from
            check_numbers = [check.number for check in checkbook.issue_check_ids]
            if check_numbers:
                next_number = max(check_numbers) + 1
            res[checkbook.id] = next_number
        return res

    _columns = {
        'name':fields.char('Name', size=30, readonly=True, required=True, states={'draft': [('readonly', False)]}),
        'issue_check_subtype':fields.selection([('deferred','Deferred'),('currents','Currents')], string='Issue Check Subtype', readonly=True, required=True, states={'draft': [('readonly', False)]}),
        'debit_journal_id': fields.many2one('account.journal','Debit Journal', help='It will be used to make the debit of the check on checks ', readonly=True, required=True, domain=[('type','=','bank')], context={'default_type':'bank'}, states={'draft': [('readonly', False)]}),
        'journal_id': fields.many2one('account.journal','Journal', help='Journal where it is going to be used', readonly=True, required=True, domain=[('type','=','bank')], context={'default_type':'bank'}, states={'draft': [('readonly', False)]}),
        'range_from': fields.integer('From Check Number', readonly=True,required=True, states={'draft': [('readonly', False)]}),
        'range_to': fields.integer('To Check Number', readonly=True, required=True, states={'draft': [('readonly', False)]}),
        'next_check_number':fields.function(_get_next_check_number, string='Next Check Number', type='char', readonly=True,),
        'padding' : fields.integer('Number Padding', help="automatically adds some '0' on the left of the 'Number' to get the required padding size."),
        'user_id' : fields.many2one('res.users','User'),
        'company_id': fields.related('journal_id','company_id', relation="res.company", type="many2one", string='Company', store=True),
        'issue_check_ids': fields.one2many('account.check','checkbook_id', string='Issue Checks', readonly=True,),
        'state':fields.selection([('draft','Draft'),('active','In Use'),('used','Used')],string='State',readonly=True),                            
    }
    
    _order = "name"
    _defaults = {
        'state': 'draft',
        'padding': 8,
    }

    def _check_numbers(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if (data.range_to <= data.range_from):
                return False
        return True

    _constraints = [
        (_check_numbers, 'Range to must be greater than range from', ['range_to','range_from']),
        ]

    def copy(self, cr, uid, id, default=None, context=None):
        default = {} if default is None else default.copy()
        context = {} if context is None else context.copy()
        record = self.browse(cr, uid, id, context=context)
        default.update({
            'state':'draft',
            'ref': False,
            'name': _("%s (copy)") % (record.name or ''),
        })
        return super(account_checkbook, self).copy(cr, uid, id, default, context)        
    
    def unlink(self, cr, uid, ids, context=None):
        for record in self.browse(cr,uid,ids,context=context):

            if  record.state not in ('draft'):
                raise osv.except_osv(_('Error !'), _('You can drop the checkbook(s) only in draft state !'))
                return False 
        return super(account_checkbook, self).unlink(cr, uid, ids, context=context) 
   
    def wkf_active(self, cr, uid, ids,context=None):
        if context is None:
            context = {}
        res= {}  
        for record in self.browse(cr,uid,ids,context=context):        
            if res:
                raise osv.except_osv(_('Error !'), _('You cant change the checkbook´s state, there is one active for this Bank Account!'))
                return False 
            else:
                self.write(cr, uid, ids, { 'state' : 'active' })
                return True
                
    def wkf_used(self, cr, uid, ids,context=None):
        self.write(cr, uid, ids, { 'state' : 'used' })
        return True

    def action_cancel_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        self.delete_workflow(cr, uid, ids)
        self.create_workflow(cr, uid, ids)        
