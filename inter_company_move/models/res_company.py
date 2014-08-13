# -*- coding: utf-8 -*-
##############################################################################
#
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

from openerp.osv import osv, fields
from openerp.tools.translate import _

class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'invoice_move_type': fields.selection([('not_available','Not Available'),('move_auto','Move Automatically')], string='Invoice Move Type', required=True),
        'open_after_move': fields.boolean('Open New Record After Move?', help="Please note that to open the new record you must have the right access rights. This is only advisible when it is moved to a child company."),
        'record_moved_id': fields.boolean('Record Moved Id', help="Please note that to open the new record you must have the right access rights. This is only advisible when it is moved to a child company."),
		'invoice_move_company_id': fields.many2one('res.company', 'Destiny Company',),
    }

    _defaults = {
    	'invoice_move_type': 'not_available', 
    }