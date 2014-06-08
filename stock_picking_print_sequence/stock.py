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

from osv import osv
from osv import fields
from tools.translate import _
import traceback

class stock_journal(osv.osv):
    _inherit = "stock.journal"
    
    _columns = {
        'sequence_id': fields.many2one('ir.sequence', 'Stock Picking Print Sequence'),
    }


class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    
    _columns = {
        'print_sequence_number': fields.char('Picking Number', size=64),
        'cant_modify_stock_journal': fields.boolean('Cant modify Stock Journal')
    }
    
    _sql_constraints = [('print_sequence_number_no_uniq','unique(print_sequence_number, company_id)',
                         _('The field "Print Sequence Number" must be unique.'))]
    
    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()
        picking = self.browse(cr, uid, id, context=context)
        default.update(print_sequence_number=False)
        # This would be to add copy
        # default.update(print_sequence_number=_("%s (copy)") % (picking['print_sequence_number'] or ''))
        return super(stock_picking_out, self).copy(cr, uid, id, default, context=context)
    
    def set_print_sequence_number(self, cr, uid, ids, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        
        sequence_obj = self.pool.get('ir.sequence')
        picking_obj = self.pool.get('stock.picking')
        
        for picking in self.browse(cr, uid, ids, context=context):
            if not picking.stock_journal_id:
                title = _('No journal defined')
                message = _('There is no journal defined for the current Picking.')
                raise osv.except_osv(title, message)
            elif not picking.stock_journal_id.sequence_id:
                title = _('No sequence defined')
                message = _('There is journal defined for the current Picking but that journal does not have any sequence defined.')
                raise osv.except_osv(title, message)
            
            sequence_id = picking.stock_journal_id.sequence_id.id
            next_seq_num = sequence_obj.next_by_id(cr, uid, sequence_id, context=context)
            picking_obj.write(cr, uid, picking.id, {'print_sequence_number': next_seq_num}, context=context)
    
    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default['print_sequence_number'] = None
        return super(stock_picking, self).copy(cr, uid, id, default=default, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        picking_obj = self.pool.get('stock.picking')
        
        for picking in picking_obj.browse(cr, uid, ids, context=context):
            state = False
            if 'state' in vals:
                state = vals['state']
            else:
                state = picking.state
        
        return super(stock_picking, self).write(cr, uid, ids, vals, context=context)

# Redefinition of the new fields in order to update the model stock.picking.out in the orm
# FIXME: this is a temporary workaround because of a framework bug (ref: lp996816). It should be removed as soon as
#        the bug is fixed    
class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    
    _columns = {
        'print_sequence_number': fields.char('Picking Number', size=64),
        'cant_modify_stock_journal': fields.boolean('Cant modify Stock Journal')
    }

    def copy(self, cr, uid, id, default=None, context=None, done_list=None, local=False):
        default = {} if default is None else default.copy()
        picking = self.browse(cr, uid, id, context=context)
        default.update(print_sequence_number=False)
        # This would be to add copy
        # default.update(print_sequence_number=_("%s (copy)") % (picking['print_sequence_number'] or ''))
        return super(stock_picking_out, self).copy(cr, uid, id, default, context=context)


class stock_warehouse(osv.osv):
    _inherit = 'stock.warehouse'
    
    _columns = {
        'stock_journal_id': fields.many2one('stock.journal', 'Stock Journal'),
    }





















