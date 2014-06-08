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
from lxml import etree
from openerp.osv import fields, osv
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.float_utils import float_compare
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class stock_partial_picking(osv.osv_memory):
   
    _inherit = "stock.partial.picking"

    def _get_max_lines(self, cr, uid, context=None):
        if context is None: context = {}
        picking_obj = self.pool.get('stock.picking.out')
        id = context.get('active_id', False)
        ret = False
        if id:
            report_conf = picking_obj.get_report_configuration(cr, uid, id, context=context)
            if report_conf.stock_picking_split_picking_type_out:
                ret = report_conf.stock_picking_lines_to_split
        return ret

    def _get_excess_lines(self, cr, uid, context=None):
        if context is None: context = {}
        picking_obj = self.pool.get('stock.picking.out')
        id = context.get('active_id', False)
        ret = False
        if id:
            report_conf = picking_obj.get_report_configuration(cr, uid, id, context=context)
            if report_conf.stock_picking_split_picking_type_out:
                picking = picking_obj.browse(cr, uid, id, context=context)
                ret = len(picking.move_lines) - report_conf.stock_picking_lines_to_split
        return ret

    def _get_allow_dont_split(self, cr, uid, context=None):
        if context is None: context = {}
        picking_obj = self.pool.get('stock.picking')
        id = context.get('active_ids', False)
        ret = False
        if id:
            report_conf = picking_obj.get_report_configuration(cr, uid, id, context=context)
            if report_conf.stock_picking_split_picking_type_out:
                ret = report_conf.stock_picking_dont_split_option
        return ret        

    _columns = {
        'excess_lines' : fields.integer(string='Excess Lines', readonly=True),
        'max_lines' : fields.integer(string='Maximum number of lines', help='Maximum number of lines allowed by the report', readonly=True),
        'allow_dont_split' : fields.boolean(string='Allow Dont Split', readonly=True),
        'remove_excess_lines' : fields.boolean(string='Remove Excess Lines'),
        'dont_split' : fields.boolean(string="Don't Split"),
    }

    _defaults = {
        'max_lines': _get_max_lines,
        'excess_lines': _get_excess_lines,
        'allow_dont_split': _get_allow_dont_split,
    }

    def onchange_remove_excess_lines(self, cr, uid, ids, remove_excess_lines, max_lines, move_ids, context=None):
        if context is None: context = {}
        ret = {}
        defaults = self.default_get(cr, uid, ['move_ids'], context=context)
        move_ids = defaults.get('move_ids',False)
        if move_ids:
            aux = []
            aux.append([5, False, False])
            for record in move_ids:
                aux.append([0, False, record])
            ret =  {'value':
                {'move_ids':aux
                }
            }              
        if remove_excess_lines:
            ret =  {'value':
                {'move_ids':aux[:max_lines + 1]
                }
            }
        else:
            ret =  {'value':
                {'move_ids':aux
                }
            }         
        return ret                

    def onchange_dont_split(self, cr, uid, ids, dont_split, move_ids, context=None):
        if context is None: context = {}
        ret = {}
        if dont_split:      
            ret['warning'] = {'title':"Warning!",'message':"With don't split option you can process the picking with exceeded lines.\nBut later, if you need to print the picking report, it wont fit in one page!\nPlease consider it carefully!"}
        return ret          