# -*- coding: utf-8 -*-


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

