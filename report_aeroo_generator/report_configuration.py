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

class report_configuration(osv.osv):
    _name = 'report_aeroo_generator.report_configuration'
    _description = 'Configuration information to generate an Aeroo report'
    
    already_created_report_title = _('Report already created')
    already_created_report_message = _('There is another report created with the same parameters, there cannot be more than one report with the same parameters')
    
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'description': fields.text('Description', translate=True),
        'type': fields.selection([('account.invoice', 'Invoice'),
                                  ('sale.order', 'Sale Order'),
                                  ('stock.picking.out', 'Picking'),
                                  ('account.voucher', 'Accounting Voucher'),
                                  ('purchase.order', 'Purchase Order'),], 'Type', required=True),
        'line_ids': fields.one2many('report_aeroo_generator.report_configuration_line', 'report_configuration_id',
                        string='Configuration lines'),
        
        'report_xml_id': fields.many2one('ir.actions.report.xml', 'Report XML'),
        
        'print_logo': fields.selection([('no_logo', 'Do not print log'),
                                  ('company_logo', 'Company Logo'),
                                  ('specified_logo', 'Specified Logo')], 'Print Logo', required=True),
        
        'logo': fields.binary('Logo'),
        
        'use_background_image' : fields.boolean('Use Background Image'),
        'background_image': fields.binary('Background Image'),
        
        'tml_source':fields.selection([('database','Database'),
                                       ('file','File'),
                                       ('parser','Parser'),],'Template source', select=True),
        'report_rml': fields.char('Main report file path', size=256, help="The path to the main report file (depending on Report Type) or NULL if the content is in another data field"),
        'report_sxw_content_data': fields.binary('SXW content'),
        
        # account.invoice
        'account_invoice_state': fields.selection([('proforma','Pro-forma'),
                                              ('approved_invoice','Aproved Invoice')], 'Invoice State', required=False),
        'account_invoice_journal_ids': fields.many2many('account.journal', 'report_configuration_account_journal_rel',
                                        'report_configuration_id', 'journal_id', 'Journals',
                                        domain=[('type','in',['sale', 'sale_refund'])]),
        'account_invoice_tax_included': fields.boolean('Tax Included'),
        'account_invoice_tax_ids': fields.many2many('account.tax', 'report_configuration_account_tax_default_rel',
                                                    'report_configuration_id', 'tax_id', 'Taxes'),
        'account_invoice_split_invoice': fields.boolean('Split Inovice', help='If true, when validating the invoice, if it contains more than the specified number of lines, new invoices will be generated.'),
        'account_invoice_lines_to_split': fields.integer('Lines to split'),
        
        # sale.order
        'sale_order_state': fields.selection([('draft', 'Quotation'),
                                              ('progress', 'In Progress')], 'Sale Order State', required=False),
        'sale_order_shop_ids': fields.many2many('sale.shop', 'report_configuration_sale_order_shop_rel',
                                        'report_configuration_id', 'shop_id', 'Shops'),
        # stock.picking
        'stock_picking_journal_ids': fields.many2many('stock.journal', 'report_configuration_stock_journal_rel',
                                        'report_configuration_id', 'journal_id', 'Journals'),
        'stock_picking_split_picking_type_out': fields.boolean('Split Out Picking',
            help="Split the invoice if it is of type 'Out'."),
        'stock_picking_split_picking_type_in': fields.boolean('Split In Picking',
            help="Split the invoice if it is of type 'In'."),
        'stock_picking_split_picking_type_internal': fields.boolean('Split Internal Picking',
            help="Split the invoice if it is of type 'Internal'."),
        'stock_picking_lines_to_split': fields.integer('Lines to split'),
        
        # account.voucher
        'account_voucher_journal_ids': fields.many2many('account.journal', 'report_configuration_stock_voucher_journal_rel',
                                        'report_configuration_id', 'journal_id', 'Journals'),
        'account_voucher_type': fields.selection([('sale', 'Sale'),
                                                  ('purchase', 'Purchase'),
                                                  ('payment', 'Payment'),
                                                  ('receipt', 'Receipt')], 'Account Voucher Type', required=False),
    }
    
    _defaults = {
        'account_invoice_tax_included': False,
        'print_logo': 'no_logo',
        'stock_picking_split_picking_type_out': True,
        'stock_picking_split_picking_type_in': False,
        'stock_picking_split_picking_type_internal': False,
    }
    
    def update_lines_that_apply(self, cr, uid, ids, context=None):
        key_value_obj = self.pool.get('report_aeroo_generator.report_configuration_defaults')
        conf_line_obj = self.pool.get('report_aeroo_generator.report_configuration_line')
        
        all_ids = key_value_obj.search(cr, uid, [], context=context)
        for report_configuration in self.browse(cr, uid, ids, context=context):
            conf_line_name_id = {}
            for line in report_configuration.line_ids:
                conf_line_name_id[line.name] = line.id
            
            for key_value in key_value_obj.browse(cr, uid, all_ids, context=context):
                if key_value.apply_to in ['all', report_configuration.type]:
                    vals = {'name': key_value.name, 'report_configuration_id': report_configuration.id}
                    if key_value.value_type == 'text':
                        vals['value_type'] = 'text'
                        vals['value_text'] = key_value.value_text
                    elif key_value.value_type == 'boolean':
                        vals['value_type'] = 'boolean'
                        vals['value_boolean'] = key_value.value_boolean
                    
                    if conf_line_name_id.get(key_value.name, False):
                        if key_value.override_values:
                            line_id = conf_line_name_id[key_value.name]
                            conf_line_obj.write(cr, uid, [line_id], vals, context=context)
                    else:
                        conf_line_obj.create(cr, uid, vals, context=context)
    
    def create(self, cr, uid, vals, context=None):
        '''
        When a Report Configuration is created, an associated report object is created.
        '''
        ids = super(report_configuration, self).create(cr, uid, vals, context=context)
        if isinstance(ids, list):
            self.generate_report(cr, uid, ids, vals, context=context)
        else:
            self.generate_report(cr, uid, [ids], vals, context=context)
        return ids
    
    def write(self, cr, uid, ids, vals, context=None):
        '''
        When a Report Configuration is written, the associated report object is updated.
        '''
        super(report_configuration, self).write(cr, uid, ids, vals, context=context)
        if isinstance(ids, list):
            self.generate_report(cr, uid, ids, vals, context=context)
        else:
            self.generate_report(cr, uid, [ids], vals, context=context)
        return ids
    
    def unlink(self, cr, uid, ids, context=None):
        '''
        When a Report Configuration is deleted, the associated report object is deleted as well.
        '''
        report_xml_ids = []
        for report_conf in self.browse(cr, uid, ids, context=context):
            report_xml_ids.append(report_conf.report_xml_id.id)
        
        ret = super(report_configuration, self).unlink(cr, uid, ids, context=context)
        
        report_xml_obj = self.pool.get('ir.actions.report.xml')
        report_xml_obj.unlink(cr, uid, report_xml_ids, context=context)
        
        return ret
    
    def copy(self, cr, uid, id, default=None, context=None):
        '''
        When a copy of the Report Configuration is made, the report object is not copy.
        '''
        if default is None:
            default = {}
        default['report_xml_id'] = None
        return super(report_configuration, self).copy(cr, uid, id, default=default, context=context)
    
    def generate_report(self, cr, uid, ids, saved_vals, context=None):
        '''
        If the Report Configuration does not have any report already a new one is created and associated to it.
        If the report is already created the name is updated.
        '''
        report_xml_obj = self.pool.get('ir.actions.report.xml')
        ir_values_obj = self.pool.get('ir.values')
        
        # Get the pdf output object for the report
        mimetypes_obj = self.pool.get('report.mimetypes')
        mimetypes_ids = mimetypes_obj.search(cr, uid, [], context=context)
        mimetypes_xml_ids = mimetypes_obj.get_xml_id(cr, uid, mimetypes_ids, context=context)
        out_format_id = False
        for key in mimetypes_xml_ids.keys():
            xml_id_it = mimetypes_xml_ids[key]
            if xml_id_it == 'report_aeroo_ooo.report_mimetypes_pdf_odt':
                out_format_id = key
        
        for report_conf in self.browse(cr, uid, ids, context=context):
            vals = {}
            vals['name'] = report_conf.name
            
            if report_conf.type == 'account.invoice':
                vals['model'] = 'account.invoice'
                report_name = 'account_invoice_report'
                vals['report_name'] = report_name
            elif report_conf.type == 'sale.order':
                vals['model'] = 'sale.order'
                report_name = 'sale_order_report'
                vals['report_name'] = report_name
            elif report_conf.type == 'stock.picking.out':
                vals['model'] = 'stock.picking.out'
                report_name = 'stock_picking_report'
                vals['report_name'] = report_name
            elif report_conf.type == 'account.voucher':
                vals['model'] = 'account.voucher'
                report_name = 'account_voucher_report'
                vals['report_name'] = report_name
            elif report_conf.type == 'purchase.order':
                vals['model'] = 'purchase.order'
                report_name = 'purchase_order_report'
                vals['report_name'] = report_name
                
            report_xml_id = False
            
            if saved_vals.get('tml_source', False):
                vals['tml_source'] = saved_vals['tml_source']
            if saved_vals.get('report_rml', False):
                vals['report_rml'] = saved_vals['report_rml']
            if saved_vals.get('report_sxw_content_data', False):
                vals['report_sxw_content_data'] = saved_vals['report_sxw_content_data']
                
            if report_conf.report_xml_id:
                report_xml_id = report_conf.report_xml_id.id
                report_xml_obj.write(cr, uid, report_xml_id, vals, context=context)
            else:
                vals['report_type'] = 'aeroo'
                vals['type'] = 'ir.actions.report.xml'
                vals['in_format'] = 'oo-odt'
                vals['parser_state'] = 'loc'
                if 'tml_source' not in vals:
                    vals['tml_source'] = 'file'
                if 'report_rml' not in vals:
                    vals['report_rml'] = 'report_aeroo_generator/report/general_template.odt'
                
                vals['parser_loc'] = 'report_aeroo_generator/report/general_parser.py'
                if out_format_id:
                    vals['out_format'] = out_format_id
                
                report_xml_id = report_xml_obj.create(cr, uid, vals, context=context)
                self.write(cr, uid, report_conf.id, {'report_xml_id': report_xml_id}, context=context)
            
            report_name = str(report_conf.id)
            report_xml_obj.write(cr, uid, report_xml_id, {'report_name': report_name}, context=context)            

report_configuration()

class report_configuration_line(osv.osv):
    _name = 'report_aeroo_generator.report_configuration_line'
    _description = 'Line of the configuration information'
    
    _columns = {
        'name': fields.char('Key', size=256, required=True),
        'value_type': fields.selection([('text','Text'), ('boolean','Boolean')], 'Value Type', required=True),
        'value_text': fields.text('Value', required=False, translate=True),
        'value_boolean': fields.boolean('Value', required=False),
        'report_configuration_id': fields.many2one('report_aeroo_generator.report_configuration',
                        'Configuration', required=True, ondelete='cascade'),
    }
    
report_configuration_line()

class report_configuration_defaults(osv.osv):
    _name = 'report_aeroo_generator.report_configuration_defaults'
    _description = 'Line of the configuration information'
    
    _columns = {
        'name': fields.char('Key', size=256, required=True),
        'apply_to': fields.selection([('all', 'All'),
                                      ('account.invoice', 'Invoice'),
                                      ('sale.order', 'Sale Order'),
                                      ('stock.picking.out', 'Picking'),
                                      ('account.voucher', 'Accounting Voucher')], 'Apply to', required=True),
        
        'override_values': fields.boolean('Override Values', help='If true, override values in already created Aeroo Report Configuration when saved.'),
        
        'value_type': fields.selection([('text','Text'), ('boolean','Boolean')], 'Value Type', required=True),
        'value_text': fields.text('Value', required=False, translate=True),
        'value_boolean': fields.boolean('Value', required=False),
    }
    _defaults = {
        'override_values': False,
    }
    
    def create(self, cr, uid, vals, context=None):
        ids = super(report_configuration_defaults, self).create(cr, uid, vals, context=context)
        
        configuration_obj = self.pool.get('report_aeroo_generator.report_configuration')
        conf_ids = False
        if vals['apply_to'] == 'all':
            conf_ids = configuration_obj.search(cr, uid, [], context=context)
        else:
            conf_ids = configuration_obj.search(cr, uid, [('type', '=', vals['apply_to'])], context=context)
        
        configuration_obj.update_lines_that_apply(cr, uid, conf_ids, context=context)
        
        return ids
    
    def write(self, cr, uid, ids, vals, context=None):
        super(report_configuration_defaults, self).write(cr, uid, ids, vals, context=context)
        
        for default_vk in self.browse(cr, uid, ids, context=context):
            configuration_obj = self.pool.get('report_aeroo_generator.report_configuration')
            conf_ids = False
            if default_vk.apply_to == 'all':
                conf_ids = configuration_obj.search(cr, uid, [], context=context)
            else:
                conf_ids = configuration_obj.search(cr, uid, [('type', '=', default_vk.apply_to)], context=context)
            
            configuration_obj.update_lines_that_apply(cr, uid, conf_ids, context=context)
        
        return ids
    

report_configuration_defaults()



