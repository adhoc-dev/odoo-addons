# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from osv import osv
from osv import fields
from tools.translate import _

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    
    _columns = {
        'observations': fields.text(string='Observations',),
    }

class stock_picking_out(osv.osv):
    _name = 'stock.picking.out'
    _inherit = 'stock.picking.out'
    
    _columns = {
        'observations': fields.text(string='Observations',),
    }

    def get_report_configuration(self, cr, uid, ids, context=None):
        report_conf_obj = self.pool.get('report_aeroo_generator.report_configuration')
        
        picking = self.browse(cr, uid, ids, context=context)
        if isinstance(picking, list):
            picking = picking[0]
        
        report_conf = False
        
        filters = [('type','=','stock.picking.out')]
        report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
        
        for report_conf_it in report_conf_obj.browse(cr, uid, report_conf_ids, context=context):
            journal_ids = [journal.id for journal in report_conf_it.stock_picking_journal_ids]
            if not picking.stock_journal_id or picking.stock_journal_id.id in journal_ids:
                report_conf = report_conf_it
                break
        
        if not report_conf:
            report_conf = report_conf_obj.browse(cr, uid, report_conf_ids, context=context)
            if report_conf and isinstance(report_conf, list):
                report_conf = report_conf[0]
        return report_conf
    
    def print_picking(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        saved_context = context.copy()
        if ids and isinstance(ids, list):
            context['active_ids'] = ids
        else:
            context['active_ids'] = [ids]
        if ids and isinstance(ids, list):
            context['active_id'] = ids[0]
        else:
            context['active_id'] = ids
        context['active_model'] = 'stock.picking.out'
        
        report_conf = self.get_report_configuration(cr, uid, ids, context=context)
        
        if report_conf:
            if report_conf.report_xml_id:
                context['report_conf_id'] = report_conf.id
                return {'type' : 'ir.actions.report.xml',
                        'context' : context,
                        'report_name': report_conf.report_xml_id.report_name}
            else:
                return {'type' : 'ir.actions.report.xml',
                        'context' : context,
                        'report_name': 'sale.shipping'}
        else:
            return {'type' : 'ir.actions.report.xml',
                    'context' : context,
                    'report_name': 'sale.shipping'}

























