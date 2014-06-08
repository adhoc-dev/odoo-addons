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
        'receiptbook_ids': fields.many2many('account.voucher.receiptbook', 'report_configuration_receiptbook_rel',
                                        'report_configuration_id', 'receiptbook_id', 'ReceiptBooks'),
        'receipt_type': fields.selection([('payment', 'Payment'),
                                                  ('receipt', 'Receipt')], 'Receipt Type', ),    
    }
    
    _defaults = {
    }

    def get_domains(self, cr, model, record, context=None):
        domains = super(ir_actions_report, self).get_domains(cr, model, record, context=context)
        if model == 'account.voucher.receipt':    
            # Search for especific report            
            domains.append([('receipt_type','=',record.type), ('receiptbook_ids','=',record.receiptbook_id.id)])
            # Search without type
            domains.append([('receipt_type','=',False), ('receiptbook_ids','=',record.receiptbook_id.id)])
            # Search without receiptbooks and with type
            domains.append([('receipt_type','=',record.type), ('receiptbook_ids','=',False)])
            # Search without receiptbooks and without type
            domains.append([('receipt_type','=',False), ('receiptbook_ids','=',False)])
        return domains

