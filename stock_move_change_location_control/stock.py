# -*- coding: utf-8 -*-


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
























