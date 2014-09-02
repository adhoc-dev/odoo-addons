# -*- coding: utf-8 -*-
from openerp.osv import osv


class sale_order_line(osv.osv):
    _inherit = "res.partner"

    _defaults = {'user_id': lambda self, cr, uid, context: uid, }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
