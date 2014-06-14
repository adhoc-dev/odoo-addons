# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class account_journal(osv.osv):
    _name = 'account.journal'
    _inherit = 'account.journal'
    
    _columns = {
        'store_id': fields.many2one('res.store', 'Store', help='Users that are not of this store, can see this journals records but can not post or modify any entry on them.'),
    }
