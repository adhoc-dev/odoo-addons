# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class res_users(osv.osv):

    _inherit = "res.users"

    _columns = {
        'salesman_group_id': fields.many2one(
            'sale.salesman.group', 'Salesman Group', ),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
