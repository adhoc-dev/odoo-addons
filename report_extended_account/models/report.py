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
        'account_invoice_state': fields.selection([('proforma','Pro-forma'),
                                              ('approved_invoice','Aproved Invoice')], 'Invoice State', required=False),
        'account_invoice_journal_ids': fields.many2many('account.journal', 'report_account_journal_rel',
                                        'report_id', 'journal_id', 'Journals',
                                        domain=[('type','in',['sale', 'sale_refund'])]),
        'account_invoice_split_invoice': fields.boolean('Split Inovice', help='If true, when validating the invoice, if it contains more than the specified number of lines, new invoices will be generated.'),
        'account_invoice_lines_to_split': fields.integer('Lines to split'),
    }
    
    _defaults = {
    }

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(cr, model, record, context=context)
        if model == 'account.invoice':
            account_invoice_state = False
            
            # We user ignore_state to get the report to split invoice before the invoice is validated
            ignore_state = context.get('ignore_state',False)
            if ignore_state:
                account_invoice_state = ['approved_invoice', 'proforma', False]
            elif record.state in ['proforma', 'proforma2']:
                account_invoice_state = ['proforma']
            elif record.state in ['open', 'paid', 'sale']:
                account_invoice_state = ['approved_invoice']
            # Search for especific report
            domains.append([('account_invoice_state','in',account_invoice_state), ('account_invoice_journal_ids','=',record.journal_id.id)])
            # Search without state
            domains.append([('account_invoice_state','in',account_invoice_state), ('account_invoice_journal_ids','=',False)])
            # Search without journal and state
            domains.append([('account_invoice_state','=',False), ('account_invoice_journal_ids','=',record.journal_id.id)])
            # Search without journal and without state
            domains.append([('account_invoice_state','=',False), ('account_invoice_journal_ids','=',False)])
        return domains

