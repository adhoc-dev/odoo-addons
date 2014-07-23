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
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'copy_journal_id': fields.related('journal_id',relation='account.journal', type='many2one', string='Journal', required=True, readonly=True, states={'draft':[('readonly',False)]}),
    }

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,
                            date_invoice=False, payment_term=False,
                            partner_bank_id=False, company_id=False, context=None):
        result = super(account_invoice,self).onchange_partner_id(cr, uid, ids,
                       type, partner_id, date_invoice, payment_term,
                       partner_bank_id, company_id)
        
        print 'result', result
        if type == 'in_invoice':
            journal_type = 'purchase'
        elif type == 'in_refund':
            journal_type = 'purchase_refund'
        elif type == 'out_invoice':
            journal_type = 'sale'
        elif type == 'out_refund':
            journal_type = 'sale_refund'

        journal_id = False
        journal_ids = False
        normal_journal_ids = False
        
        if company_id and partner_id:
            normal_journal_ids = self.get_valid_journals(cr, uid, partner_id, journal_type, is_debit_note=False, company_id=company_id)
            journal_ids = self.get_valid_journals(cr, uid, partner_id, journal_type, company_id=company_id)

        if normal_journal_ids:            
            journal_id = normal_journal_ids[0]
        
        if 'value' not in result: result['value'] = {}
        result['value'].update({
           'copy_journal_id': journal_id,
        })      

        if 'domain' not in result: result['domain'] = {}          
        result['domain'].update({
           'copy_journal_id': [('id', 'in', journal_ids)],
        })  
        return result

    def onchange_copy_journal_id(self, cr, uid, ids, copy_journal_id, context=None):
        
        result = {}        
        result['value'] = {
           'journal_id': copy_journal_id,
           }
        return result        


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

