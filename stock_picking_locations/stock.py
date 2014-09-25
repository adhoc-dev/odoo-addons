# -*- coding: utf-8 -*-


from openerp.osv import osv
from openerp.osv import fields

class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    _class = {
        'location_id': fields.many2one('stock.location', 'Source Location', select=True, states= {'done': [('readonly', True)]},
                        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations. This will be the default of the asociated stock moves."),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location', select=True,
                            states={'done': [('readonly', True)]},
                            help="Location where the system will stock the finished products. This will be the default of the asociated stock moves."),
    }
    
    def update_locations(self, cr, uid, ids, context=None):
        move_obj = self.pool.get("stock.move")
        if not isinstance(ids, list):
            ids = [ids]
        for picking in self.browse(cr, uid, ids, context=context):
            vals = {'location_id': picking.location_id.id, 'location_dest_id': picking.location_dest_id.id}
            for move in picking.move_lines:
                move_obj.write(cr, uid, move.id, vals, context=context)
    
class stock_picking_in(osv.osv):
    _name = 'stock.picking.in'
    _inherit = 'stock.picking.in'
    
    _class = {
    }

    def update_locations(self, cr, uid, ids, context=None):
        #override in order to redirect on the stock.picking object        
        return self.pool.get('stock.picking').update_locations(cr, uid, ids, context)

class stock_picking_out(osv.osv):
    _name = 'stock.picking.out'
    _inherit = 'stock.picking.out'
    
    _class = {
    }

    def update_locations(self, cr, uid, ids, context=None):
        #override in order to redirect on the stock.picking object        
        return self.pool.get('stock.picking').update_locations(cr, uid, ids, context)

#  No lo estamos usando por ahora este metodo

# class stock_move(osv.osv):
#     _name = 'stock.move'
#     _inherit = 'stock.move'
    
#     def _default_location_source_2(self, cr, uid, context=None):
#         location_id = context.get('location_id', False)
#         if location_id:
#             return location_id
#         else:
#             return super(stock_move, self)._default_location_source(cr, uid, context=context)
    
#     def _default_location_destination_2(self, cr, uid, context=None):
#         location_dest_id = context.get('location_dest_id', False)
#         if location_dest_id:
#             return location_dest_id
#         else:
#             return super(stock_move, self)._default_location_destination(cr, uid, context=context)
    
#     _defaults = {
#         'location_id': _default_location_source_2,
#         'location_dest_id': _default_location_destination_2,
#     }

# stock_move()
























