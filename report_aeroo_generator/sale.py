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
from openerp import netsvc
from tools.translate import _
from openerp import pooler

class sale_order(osv.osv):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    def print_order(self, cr, uid, ids, context=None):
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
        context['active_model'] = 'sale.order'
        
        report_conf_obj = self.pool.get('report_aeroo_generator.report_configuration')
        
        order = self.browse(cr, uid, ids, context=context)
        if isinstance(order, list):
            order = order[0]
        
        sale_order_state = False
        if order.state in ['draft','sent']:
            sale_order_state = 'draft'
        elif order.state not in ['draft', 'cancel','sent']:
            sale_order_state = 'progress'
        
        report_conf = False
        
        filters = [('type','=','sale.order'), ('sale_order_state','=',sale_order_state)]
        report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
        
        for report_conf_it in report_conf_obj.browse(cr, uid, report_conf_ids, context=context):
            shop_ids = [shop.id for shop in report_conf_it.sale_order_shop_ids]
            if order.shop_id.id in shop_ids:
                report_conf = report_conf_it
                break
        
        if not report_conf:
            if report_conf_ids:
                report_conf = report_conf_obj.browse(cr, uid, report_conf_ids, context=context)
                if report_conf and isinstance(report_conf, list):
                    report_conf = report_conf[0]
        
        if not report_conf:
            filters = [('type','=','sale.order')]
            report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
            
            for report_conf_it in report_conf_obj.browse(cr, uid, report_conf_ids, context=context):
                shop_ids = [shop.id for shop in report_conf_it.sale_order_shop_ids]
                if order.shop_id.id in shop_ids:
                    report_conf = report_conf_it
                    break
        
        if not report_conf:
            filters = [('type','=','sale.order')]
            report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
            if report_conf_ids:
                report_conf = report_conf_obj.browse(cr, uid, report_conf_ids, context=context)
                if report_conf and isinstance(report_conf, list):
                    report_conf = report_conf[0]

# Esto lo robe del modulo sale y es para marcar que ya se imprimio la sale order
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)

        
        if report_conf:
            if report_conf.report_xml_id:
                context['report_conf_id'] = report_conf.id
                return {'type' : 'ir.actions.report.xml',
                        'context' : context,
                        'report_name': report_conf.report_xml_id.report_name}
            else:
                return {'type' : 'ir.actions.report.xml',
                        'context' : context,
                        'report_name': 'sale.order'}
        else:
            return {'type' : 'ir.actions.report.xml',
                    'context' : context,
                    'report_name': 'sale.order'}
'''    
    def manual_invoice(self, cr, uid, ids, context=None):
        ret = super(sale_order, self).manual_invoice(cr, uid, ids, context=context)
        
        new_context = ret.get('context', False)
        
        if not new_context:
            new_context = {}
        elif not isinstance(new_context, dict):
            try:
                new_context = eval(new_context)
            except:
                new_context = {}
        
        active_id = ret.get('res_id', False)
        if active_id:
            new_context['active_id'] = active_id
            new_context['active_ids'] = [active_id]
        
        new_context['active_model'] = 'account.invoice'
        
        context.update(new_context)
        
        ret.update({'context': context})
        
        
        return ret
'''
sale_order()


























