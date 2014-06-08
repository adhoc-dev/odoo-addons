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

class partner(osv.osv):
    _inherit = 'res.partner'

    # def _get_related_user(self, cr, uid, ids, field_names, arg, context=None):
    #     res = {}
    #     for record in self.browse(cr, uid, ids, context=context):
    #         res[record.id] = record.user_ids
    #     return res

    _columns = {
        # 'related_user_id': fields.function(_get_related_user, relation='res.users', type="many2one", string="Related User", readonly=True,),        
    # Aparentemente no es necesario el campo m2o para el related, podemos llegar a traves del o2m
        # 'is_employee': fields.related('related_user_id', 'is_employee', string='Is Employee?', type="boolean", readonly=True, help="If user belongs to employee group return True"),
        'is_employee': fields.related('user_ids', 'is_employee', string='Is Employee?', type="boolean", readonly=True, help="If user belongs to employee group return True"),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
