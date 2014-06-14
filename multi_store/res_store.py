# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import SUPERUSER_ID

class res_store(osv.osv):
    _name = "res.store"
    _description = 'Stores'
    _order = 'parent_id desc, name'
        
    _columns = {
        'name': fields.char('Name', size=128, required=True,),
        'parent_id': fields.many2one('res.store', 'Parent Store', select=True),
        'child_ids': fields.one2many('res.store', 'parent_id', 'Child Stores'),
        'journal_ids': fields.one2many('account.journal', 'store_id', 'Journals'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'user_ids': fields.many2many('res.users', 'res_store_users_rel', 'cid', 'user_id', 'Accepted Users'),
    }
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The company name must be unique !')
    ]

    _defaults = {
        'company_id': lambda self, cr, uid, ctx: self.pool['res.company']._company_default_get(cr, uid, 'res.store', context=ctx),
    }

    _constraints = [
        (osv.osv._check_recursion, 'Error! You can not create recursive stores.', ['parent_id'])
    ]

    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        if context.pop('user_preference', None):
            # We browse as superuser. Otherwise, the user would be able to
            # select only the currently visible companies (according to rules,
            # which are probably to allow to see the child companies) even if
            # she belongs to some other companies.
            user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context=context)
            cmp_ids = list(set([user.store_id.id] + [cmp.id for cmp in user.store_ids]))
            uid = SUPERUSER_ID
            args = (args or []) + [('id', 'in', cmp_ids)]
        return super(res_store, self).name_search(cr, uid, name=name, args=args, operator=operator, context=context, limit=limit)
