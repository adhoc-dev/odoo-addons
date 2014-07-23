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

class account_voucher(osv.osv):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    def print_voucher(self, cr, uid, ids, context=None):
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
        context['active_model'] = 'account.voucher'
        
        report_conf_obj = self.pool.get('report_aeroo_generator.report_configuration')
        
        voucher = self.browse(cr, uid, ids, context=context)
        if isinstance(voucher, list):
            voucher = voucher[0]
        
        report_conf = False
        
        filters = [('type','=','account.voucher'), ('account_voucher_type','=',voucher.type)]
        report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
        
        for report_conf_it in report_conf_obj.browse(cr, uid, report_conf_ids, context=context):
            journal_ids = [journal.id for journal in report_conf_it.account_voucher_journal_ids]
            if voucher.journal_id.id in journal_ids:
                report_conf = report_conf_it
                break
        
        if not report_conf:
            if report_conf_ids:
                report_conf = report_conf_obj.browse(cr, uid, report_conf_ids, context=context)
                if report_conf and isinstance(report_conf, list):
                    report_conf = report_conf[0]
        
        if not report_conf:
            filters = [('type','=','account.voucher')]
            report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
            
            for report_conf_it in report_conf_obj.browse(cr, uid, report_conf_ids, context=context):
                journal_ids = [journal.id for journal in report_conf_it.account_voucher_journal_ids]
                if voucher.journal_id.id in journal_ids:
                    report_conf = report_conf_it
                    break
        
        if not report_conf:
            filters = [('type','=','account.voucher')]
            report_conf_ids = report_conf_obj.search(cr, uid, filters, context=context)
            if report_conf_ids:
                report_conf = report_conf_obj.browse(cr, uid, report_conf_ids, context=context)
                if report_conf and isinstance(report_conf, list):
                    report_conf = report_conf[0]
        
        title = _('No report defined')
        message = _('There is no report defined for Accounting Voucher with this parameters or for Accounting Voucher in general.')
        if report_conf:
            if report_conf.report_xml_id:
                context['report_conf_id'] = report_conf.id
                return {'type' : 'ir.actions.report.xml',
                        'context' : context,
                        'report_name': report_conf.report_xml_id.report_name}
            else:
                raise osv.except_osv(title, message)
        else:
            raise osv.except_osv(title, message)
    
        
account_voucher()
























