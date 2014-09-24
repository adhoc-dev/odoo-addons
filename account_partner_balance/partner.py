# -*- coding: utf-8 -*-


from operator import itemgetter
import time

from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _balance(self, cr, uid, ids, field_name, args,context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=None):
            res[line.id] = line.debit + line.credit
        return res

    _columns = {
        # 'net': fields.function(_net, store={'account.move.line': (lambda self, cr, uid, ids, c={}: ids,
                # ['debit', 'credit'],10)}, method=True, string='Net'),     
        # quise hacer la funcion con store pero el problema es que solo me calcula cuando modifico un campo y no me hace el calculo la primer vez
        'balance': fields.function(_balance, string='Balance'),        
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
