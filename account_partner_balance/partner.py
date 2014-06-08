# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
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
