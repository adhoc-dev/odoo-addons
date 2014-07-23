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

class stock_journal(osv.osv):
    _name = 'stock.journal'
    _inherit = 'stock.journal'
    
    _columns = {
        'user_ids': fields.many2many('res.users', 'location_security_stock_journal_users', 'journal_id', 'user_id', 'Users'),
    }
        
stock_journal()

class stock_location(osv.osv):
    _name = 'stock.location'
    _inherit = 'stock.location'
    
    _columns = {
        'user_ids': fields.many2many('res.users', 'location_security_stock_location_users', 'location_id', 'user_id', 'Users'),
    }
    
    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        group_obj = self.pool.get('res.groups')
        user_obj = self.pool.get('res.users')
        
        if group_obj.user_in_group(cr, uid, uid, 'location_security.restrict_locations', context=context):
            for move in self.browse(cr, uid, ids, context=context):
                title = _('Invalid Location')
                message = _('You cannot process this move since it is in a location you do not control.')
                if not user_obj.can_move_stock_to_location(cr, uid, move.location_id.id, context=context):
                    raise osv.except_osv(title, message)
                if not user_obj.can_move_stock_to_location(cr, uid, move.location_dest_id.id, context=context):
                    raise osv.except_osv(title, message)
        
stock_location()


class stock_picking(osv.osv):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    def force_assign(self, cr, uid, ids, *args):
        stock_move_obj = self.pool.get('stock.move')
        for pick in self.browse(cr, uid, ids):
            move_ids = [x.id for x in pick.move_lines if x.state in ['confirmed','waiting']]
            stock_move_obj.check_location_security_constrains(cr, uid, move_ids)
        return super(stock_picking, self).force_assign(cr, uid, ids, args)

stock_picking()


class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'
    
    def do_partial(self, cr, uid, ids, partial_datas, context=None):
        self.check_location_security_constrains(cr, uid, ids, context=context)
        return super(stock_move, self).do_partial(cr, uid, ids, partial_datas, context=context)
    
    def force_assign(self, cr, uid, ids, context=None):
        self.check_location_security_constrains(cr, uid, ids, context=context)
        return super(stock_move, self).force_assign(cr, uid, ids, context=context)
    
    def action_done(self, cr, uid, ids, context=None):
        self.check_location_security_constrains(cr, uid, ids, context=context)
        return super(stock_move, self).action_done(cr, uid, ids, context=context)
    
    def check_location_security_constrains(self, cr, uid, ids, context=None):
        group_obj = self.pool.get('res.groups')
        user_obj = self.pool.get('res.users')
        
        if group_obj.user_in_group(cr, uid, uid, 'location_security.restrict_locations', context=context):
            for move in self.browse(cr, uid, ids, context=context):
                title = _('Invalid Location')
                message = _('You cannot process this move since you do not control the location "%s".')
                if not user_obj.can_move_stock_to_location(cr, uid, move.location_id.id, context=context):
                    raise osv.except_osv(title, message % move.location_id.name)
                if not user_obj.can_move_stock_to_location(cr, uid, move.location_dest_id.id, context=context):
                    raise osv.except_osv(title, message % move.location_id.name)
    
stock_move()
