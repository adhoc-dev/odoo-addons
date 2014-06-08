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

from openerp.osv import osv, fields
from openerp.tools.translate import _

class account_invoice(osv.osv):
    _name = 'account.invoice'

    def _get_inter_document_type(self, cr, uid, ids, name, args, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            inter_document_type = False              
            for inter_document in record.company_id.intercompany_document_ids:
                if inter_document.model == 'invoice':
                    inter_document_type = inter_document.type
                    break
            res[record.id] = inter_document_type
        return res    

    _columns = {
        'inter_document_type': fields.function(_get_inter_document_type, type='char', string='Intercompany Document Type',),
    }

    def move_document(self, cr, uid, ids, context=None):
        # Todo this 
        for record in self.browse(cr, uid, ids, context=context):
            if record.inter_document_type == 'move_auto':
                return self._move_document(cr, uid, ids, record.destiny_company_id, context=context)
            elif record.inter_document_type == 'move_wizard'
                return "window_action"
            
    def _move_document(self, cr, uid, ids, destiny_company_id, context=None):

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
