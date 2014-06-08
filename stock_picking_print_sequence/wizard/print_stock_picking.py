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

from osv import fields, osv

class print_stock_picking(osv.osv_memory):
    _name = 'print_stock_picking'
    _description = "Print Stock Picking"

    _columns = {
        'print_sequence_number': fields.char('Print Sequence Number', size=64),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        res = super(print_stock_picking, self).default_get(cr, uid, fields, context=context)        
        
        if 'active_id' not in context:
            return res
        
        picking_obj = self.pool.get('stock.picking')
        picking_id = context['active_id']
        picking = picking_obj.browse(cr, uid, picking_id, context=context)
        if isinstance(picking, list):
            picking = picking[0]
            
        if not picking.print_sequence_number:
            picking_obj.set_print_sequence_number(cr, uid, picking_id, context=context)
            picking = picking_obj.browse(cr, uid, picking_id, context=context)
        
        res['print_sequence_number'] = picking.print_sequence_number
        return res
    
    def recompute_sequence_number(self, cr, uid, ids, context=None):
        if 'active_id' not in context:
            return False
        
        picking_obj = self.pool.get('stock.picking')
        picking_id = context['active_id']
        picking = picking_obj.browse(cr, uid, picking_id, context=context)
        if isinstance(picking, list):
            picking = picking[0]
            
        picking_obj.set_print_sequence_number(cr, uid, picking_id, context=context)
        picking = picking_obj.browse(cr, uid, picking_id, context=context)
        
        vals = {'print_sequence_number': picking.print_sequence_number}
        return {'value': vals}
    
    def print_stock_picking(self, cr, uid, ids, context=None):
        picking_obj = self.pool.get('stock.picking.out')
        
        if 'active_id' not in context:
            return False
        picking_id = context['active_id']
        
        ret = picking_obj.print_picking(cr, uid, picking_id, context=context)
        picking_obj.write(cr, uid, picking_id, {'cant_modify_stock_journal': True}, context=context)
        return ret 
