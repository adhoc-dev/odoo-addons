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
import logging
import netsvc


_logger = logging.getLogger(__name__)

class purchase_order(osv.osv):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    
    def get_report_configuration(self, cr, uid, ids, context=None):
        report_conf_obj = self.pool.get('report_aeroo_generator.report_configuration')
        
        purchase_order = self.browse(cr, uid, ids, context=context)
        if isinstance(purchase_order, list):
            purchase_order = purchase_order[0]
        
        report_conf = False
        
        filters = [('type','=','purchase.order')]
        report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
        report_conf = report_conf_obj.browse(cr, uid, report_conf_ids, context=context)
        if report_conf and isinstance(report_conf, list):
            report_conf = report_conf[0]
        
        return report_conf
    
    def print_order(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        saved_context = context.copy()
# esta linea la robe de purchase y es para indicar que el reporte ya se imprimio        
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'purchase.order', ids[0], 'send_rfq', cr)
        if ids and isinstance(ids, list):
            context['active_ids'] = ids
        else:
            context['active_ids'] = [ids]
        if ids and isinstance(ids, list):
            context['active_id'] = ids[0]
        else:
            context['active_id'] = ids
        context['active_model'] = 'purchase.order'
        
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
                        'report_name': 'purchase.order'}
        else:
            return {'type' : 'ir.actions.report.xml',
                    'context' : context,
                    'report_name': 'purchase.order'}
    
    
    
purchase_order()
























