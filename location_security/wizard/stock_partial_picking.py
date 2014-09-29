# -*- coding: utf-8 -*-


import time
from osv import fields, osv
from tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import decimal_precision as dp
from tools.translate import _

class stock_partial_picking(osv.osv_memory):
    _name = 'stock.partial.picking'
    _inherit = 'stock.partial.picking'

    def do_partial(self, cr, uid, ids, context=None):
        group_obj = self.pool.get('res.groups')
        user_obj = self.pool.get('res.users')
        
        if group_obj.user_in_group(cr, uid, uid, 'location_security.restrict_locations', context=context):
            for partial in self.browse(cr, uid, ids, context=context):
                for wizard_line in partial.move_ids:
                    title = _('Invalid Location')
                    message = _('You cannot process this move since it is in a location you do not control.')
                    if not user_obj.can_move_stock_to_location(cr, uid, wizard_line.location_id.id, context=context):
                        raise osv.except_osv(title, message)
                    if not user_obj.can_move_stock_to_location(cr, uid, wizard_line.location_dest_id.id, context=context):
                        raise osv.except_osv(title, message)
        return super(stock_partial_picking, self).do_partial(cr, uid, ids, context=context)

stock_partial_picking()
