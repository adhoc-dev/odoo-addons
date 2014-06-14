# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class res_users(osv.osv):
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

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on
        store fields. Access rights are disabled by
        default, but allowed on some specific fields defined in
        self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(res_users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.append('store_id')
        # duplicate list to avoid modifying the original reference
        self.SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        self.SELF_READABLE_FIELDS.append('store_id')
        return init_res    
