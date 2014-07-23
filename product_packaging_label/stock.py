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

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    # _inherit = 'stock.move'
    
    def _get_packages_qty(self, cr, uid, ids, name, args, context=None):
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            packages = 0
            for line in obj.move_lines:
                labels = len(line.product_id.packaging_label_ids)
                packages += labels * line.product_qty or 0
            result[obj.id] = packages
        return result
    
    _columns = {
        'packages_qty': fields.function(_get_packages_qty, type='integer', string="Packages Quantity", readonly=True, ),
    }


class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'
    
    def _get_packages_qty(self, cr, uid, ids, context=None):
        return self.pool.get('stock.picking')._get_packages_qty(cr, uid, ids, context=context)
    
    _columns = {
        'packages_qty': fields.function(_get_packages_qty, type='integer', string="Packages Quantity", readonly=True, ),
    }


















