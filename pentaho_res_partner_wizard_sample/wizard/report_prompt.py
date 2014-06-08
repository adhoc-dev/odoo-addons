import io
import os
import xmlrpclib
import base64
import time
from lxml import etree

from datetime import date, datetime
import pytz

from osv import osv, fields

from tools import config
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from tools.translate import _

from pentaho_reports.core import DEFAULT_OUTPUT_TYPE

# MOD: Parameters 
model = 'res.partner'
report_name = 'res_partner_report_sample'  #defined in this module report/report_data.xml
#---------------------------------------------------------------------------------------------------------------



class res_partner_report_sample(osv.osv_memory): # MOD

    _name = "res.partner.report.sample" # MOD
    _description = "Res Partner Report Sample" # MOD

    _columns = {
                'output_type' : fields.selection([('pdf', 'Portable Document (pdf)'),('xls', 'Excel Spreadsheet (xls)'),('csv', 'Comma Separated Values (csv)'),\
                                                  ('rtf', 'Rich Text (rtf)'), ('html', 'HyperText (html)'), ('txt', 'Plain Text (txt)')],\
                                                  'Report format', help='Choose the format for the output', required=True),
# MOD: columns here
                'name': fields.char('Name Like', size=64),
                'parent_name': fields.char('Parent Name', size=64),
                'category_ids': fields.many2many('res.partner.category', id1='partner_id', id2='category_id', string='Tags'),
                'date': fields.date('Date From'),
                'customer': fields.selection([('yes', 'Yes'), ('no', 'No')],'Customer',),
                'supplier': fields.selection([('yes', 'Yes'), ('no', 'No')],'Supplier',),
                'user_id': fields.many2one('res.users', 'Salesperson',),
                'country_id': fields.many2one('res.country', 'Country'),
                'credit': fields.float(string='Total Receivable greater than'),
                }

    def _get_output_type(self, cr, uid, context=None):
        
        if context is None:
            context = {}
        reports_obj = self.pool.get('ir.actions.report.xml')
        domain = [('report_name','=',report_name)]
        report_id = reports_obj.search(cr, uid, domain, limit=1)
        res = reports_obj.browse(cr, uid, report_id, context=context)[0].pentaho_report_output_type
        return res

    _defaults = {
        'output_type': _get_output_type,
# MOD: adds defaults if neccesariy    
    }

    def check_report(self, cr, uid, ids, context=None):

        wizard = self.browse(cr, uid, ids[0], context=context)
        
        if context is None:
            context = {}
        data = {}

        obj_model = self.pool.get(model)
        filters = []

# MOD: filters here

        # Name
        if wizard.name:
            filters.append(('name','ilike', wizard.name))

        # Parent Name
        if wizard.name:
            filters.append(('parent_name','ilike', wizard.name))            

        # Tags 
        if wizard.category_ids:
            filters.append(('category_id','in', [x.id for x in wizard.category_ids]))          

        # Customer selection
        if wizard.customer == 'yes':
            filters.append(('customer','=',True))
        elif wizard.customer == 'no':
            filters.append(('customer','=',False))
        
        # Supplier selection
        if wizard.supplier == 'yes':
            filters.append(('supplier','=',True))
        elif wizard.supplier == 'no':
            filters.append(('supplier','=',False))       

        # Date from
        if wizard.date:
            filters.append(('date','>=', [wizard.date]))

        # User 
        if wizard.user_id:
            filters.append(('user_id','=', wizard.user_id.id)) 

        # Total Receivable
        if wizard.credit:
            filters.append(('credit','>', wizard.credit)) 

        # Country
        if wizard.country_id:
            filters.append(('country_id','=', wizard.country_id.id))
        
# No more modifications        
        model_ids = obj_model.search(cr, uid, filters, context=context)        
        if not model_ids:
            raise osv.except_osv(_('No Data!'),
                            _('There is no data for current filters.'))
        data['ids'] = model_ids
        data['model'] = model
        data['output_type'] = wizard.output_type
#        data['variables'] = self._set_report_variables(wizard)

        return self._print_report(cr, uid, ids, data, context=context)


    def _print_report(self, cr, uid, ids, data, context=None):

        if context is None:
            context = {}

        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'datas': data,
    }



