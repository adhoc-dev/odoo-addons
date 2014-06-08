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

from openerp.osv import osv, fields
from openerp.tools.translate import _

class ir_actions_report(osv.Model):
    _inherit = 'ir.actions.report.xml'
    
    _columns = {
        'stock_picking_type_ids': fields.many2many('stock.picking.type', 'report_configuration_stock_picking_type_rel',
                                        'report_configuration_id', 'picking_type_id', 'Picking Types'),
        'stock_picking_split_picking_type_out': fields.boolean('Split Out Picking',
            help="Split picking if type operation is 'Out'."),
        'stock_picking_split_picking_type_in': fields.boolean('Split In Picking',
            help="Split picking if type operation is 'In'."),
        'stock_picking_split_picking_type_internal': fields.boolean('Split Internal Picking',
            help="Split picking if type operation is 'Internal'."),
        'stock_picking_lines_to_split': fields.integer('Lines to split'),
        'stock_picking_dont_split_option': fields.boolean('Dont Split Option',
            help="Add a 'Don't Split' option on picking that should be splitted."),
    }
    
    _defaults = {
    }

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(cr, model, record, context=context)
        if model == 'stock.picking':            
            # Search for especific report
            domains.append([('stock_picking_type_ids','=',record.picking_type_id.id)])
            # Search without picking_type
            domains.append([('stock_picking_type_ids','=',False)])
        return domains

