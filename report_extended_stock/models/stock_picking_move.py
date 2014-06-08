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

from osv import fields, osv
from tools.translate import _

class stock_partial_picking(osv.osv_memory):
    _name = "stock.partial.picking"
    _inherit = 'stock.partial.picking'
    
    def do_partial(self, cr, uid, ids, context=None):
        picking_obj = self.pool.get('stock.picking.out')
        partial = self.browse(cr, uid, ids[0], context=context)
        
        report_conf = picking_obj.get_report_configuration(cr, uid, partial.picking_id, context=context)
        
        split_if_type = []
        if report_conf:
            if report_conf.stock_picking_split_picking_type_out:
                split_if_type.append('out')
            if report_conf.stock_picking_split_picking_type_in:
                split_if_type.append('in')
            if report_conf.stock_picking_split_picking_type_internal:
                split_if_type.append('internal')
        
        if report_conf and partial.picking_id and partial.picking_id.type in split_if_type and not partial.dont_split:
            # Removed ths condition because it seams not neccesary
            # if partial.picking_id.stock_journal_id and partial.picking_id.stock_journal_id in report_conf.stock_picking_journal_ids:
            if report_conf.stock_picking_lines_to_split:
                if len(partial.move_ids) > report_conf.stock_picking_lines_to_split:
                    title = _('Max. lines exceeded')
                    message = _('You can validate at most %s lines. Try validating some of them and the validate the remaining moves.')
                    raise osv.except_osv(title, message % report_conf.stock_picking_lines_to_split)
        
        super(stock_partial_picking, self).do_partial(cr, uid, ids, context=context)
        return {'type': 'ir.actions.act_window_close'}

stock_partial_picking()

