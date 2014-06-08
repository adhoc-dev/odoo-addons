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

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'
    
    def write(self, cr, uid, ids, vals, context=None):
        if 'location_id' in vals:
            vals_state = vals.get('state', False)
            
            if not isinstance(ids, list):
                ids = [ids]
            
            for move in self.browse(cr, uid, ids, context=context):
                state = vals_state
                if not state:
                    state = move.state
                
                if state and state == 'assigned':
                    if 'state' in vals:
                        del vals['state']
                    self.write(cr, uid, [move.id], {'state': 'confirmed'}, context=context)
        
        return  super(stock_move, self).write(cr, uid, ids, vals, context=context)
    
stock_move()
























