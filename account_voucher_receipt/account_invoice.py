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

from openerp.osv import osv
from openerp.tools.translate import _

class invoice(osv.osv):
    _inherit = 'account.invoice'

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        if not ids: return []
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        action_receipt = mod_obj.get_object_reference(cr, uid, 'account_voucher_receipt', 'receipts_list_action')
        action_receipt = action_receipt and action_receipt[1] or False

        inv = self.browse(cr, uid, ids[0], context=context)
        partner_id = self.pool.get('res.partner')._find_accounting_partner(inv.partner_id).id
        new_context = {
                'payment_expected_currency': inv.currency_id.id,
                'default_partner_id': partner_id,
                'default_supplier_id': partner_id,
                'default_customer_id': partner_id,
                'receipt_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                # 'default_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                # 'amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
                'default_reference': inv.name,
                # TODO analyse
                'close_after_process': True,
                'invoice_type': inv.type,
                'invoice_id': inv.id,
                'default_type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
                'type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment'
            }
        action_receipt = act_obj.read(cr, uid, [action_receipt], context=context)[0]
        action_receipt['target'] = 'current'
        action_receipt['context'] = new_context
        action_receipt['views'] = [action_receipt['views'][1],action_receipt['views'][0]]
        return action_receipt

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
