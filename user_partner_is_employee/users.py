# -*- coding: utf-8 -*-


from operator import itemgetter
import time

from openerp.osv import fields, osv

class users(osv.osv):
    _inherit = 'res.users'

    def _get_is_employee(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for i in ids:
            res[i] = self.user_has_groups(cr, i, 'base.group_user', context=context)
        return res

    _columns = {
        'is_employee': fields.function(_get_is_employee, string='Is Employee?', type='boolean', readonly=True, help="If user belongs to employee group return True", store=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
