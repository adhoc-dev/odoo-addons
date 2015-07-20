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

from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class res_partner_source(osv.osv):
    _name = "res.partner.source"
    _description = "Partner Source"
    _order = "name"

    _columns = {
        'name': fields.char('Name', required=True, translate=True),
    }


class res_partner(osv.osv):
    _inherit = "res.partner"

    _columns = {
    	'source_id': fields.many2one('res.partner.source', string='Source',),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
