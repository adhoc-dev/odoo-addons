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

class users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    
    _columns = {
        'stock_journal_ids': fields.many2many('stock.journal', 'location_security_stock_journal_users',
                                              'user_id', 'journal_id', 'Stock Journals'),
        'stock_location_ids': fields.many2many('stock.location', 'location_security_stock_location_users',
                                              'user_id', 'location_id', 'Stock Locations'),
    }
    
    def can_move_stock_to_location(self, cr, uid, location_id , context=None):
        user = self.browse(cr, uid, uid, context=context)
        for stock_location in user.stock_location_ids:
            if stock_location.id == location_id:
                return True
        return False
        
users()

