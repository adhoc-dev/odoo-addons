# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class users(osv.osv):
    _name = 'res.users'
    _inherit = 'res.users'
    
    _columns = {
        # Special behavior for this field: res.store.search() will only return the stores
        # available to the current user (should be the user's stores?), when the user_preference
        # context is set.
        'store_id': fields.many2one('res.store', 'Store', required=True,
            help='The store this user is currently working for.', context={'user_preference': True}),
        'store_ids':fields.many2many('res.store','res_store_users_rel','user_id','cid','Stores'),
    }

    # def _get_company(self,cr, uid, context=None, uid2=False):
    #     if not uid2:
    #         uid2 = uid
    #     user = self.pool['res.users'].read(cr, uid, uid2, ['company_id'], context)
    #     company_id = user.get('company_id', False)
    #     return company_id and company_id[0] or False

    # def _get_companies(self, cr, uid, context=None):
    #     c = self._get_company(cr, uid, context)
    #     if c:
    #         return [c]
    #     return False
        
    # _defaults = {
    #     'store_id': _get_store,
    #     'store_ids': _get_stores,
    # }

