# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP SA (<http://openerp.com>).
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
