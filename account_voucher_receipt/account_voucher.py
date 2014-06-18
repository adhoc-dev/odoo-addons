# -*- coding: utf-8 -*-
##############################################################################
#
#    Ingenieria ADHOC - ADHOC SA
#    https://launchpad.net/~ingenieria-adhoc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import netsvc


class account_voucher(osv.osv):

	_inherit = "account.voucher"
	_columns = {
		'receipt_id':fields.many2one('account.voucher.receipt', string='Receipt', required=False, readonly=True,),
		'receipt_state': fields.related('receipt_id','state',string='Receipt State', type='char',),
		'move_ids': fields.related('move_id','line_id', type='one2many', relation='account.move.line', string='Journal Items', readonly=True),
		}

	_defaults = {
	}

	def copy(self, cr, uid, id, default=None, context=None):
		if not context:
			context = {}
		default.update({
			'receipt_id': False,
			})
		return super(account_voucher, self).copy(cr, uid, id, default, context)	
	
	def cancel_voucher(self, cr, uid, ids, context=None):
		''' Mofication of cancel voucher so it cancels the receipts when voucher is cancelled'''

		super(account_voucher, self).cancel_voucher(cr, uid, ids, context)
		for voucher in self.browse(cr, uid, ids, context=context):
			if voucher.receipt_id and voucher.receipt_id.state != 'draft':
				self.pool['account.voucher.receipt'].cancel_receipt(cr, uid, [voucher.receipt_id.id], context=context)
		return True
		
	def action_cancel_draft(self, cr, uid, ids, context=None):
		super(account_voucher, self).action_cancel_draft(cr, uid, ids, context)
		for voucher in self.browse(cr, uid, ids, context=context):
			if voucher.receipt_id:
				self.pool['account.voucher.receipt'].action_cancel_draft(cr, uid, [voucher.receipt_id.id], context=context)
		return True		

	def close_receipt(self, cr, uid, ids, context=None):
		# TODO this function should be only called for one id
		voucher = self.browse(cr, uid, ids[0], context=context)
		receipt_obj = self.pool['account.voucher.receipt']
		receipt_id = voucher.receipt_id.id
		if voucher.receiptbook_id.sequence_type == 'manual' or voucher.receipt_id.origin_voucher_id.id != voucher.id:
			view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_voucher_receipt', 'receipt_validate_finish_form')
			view_id = view_ref and view_ref[1] or False,
			return {
				'name': _('Receipt'),
				'view_type': 'form',
				'view_mode': 'form',
				'view_id': view_id,
				'res_model': 'account.voucher.receipt',
				'type': 'ir.actions.act_window',
				'nodestroy': True,
				'target': 'inline',
				'target': 'new',
				'res_id': receipt_id,
			}		
		else:
			receipt_obj.post_receipt(cr, uid, [receipt_id], context=context)
			return True

	def validate_voucher(self, cr, uid, ids, context=None):
		self.create_or_add_receipt(cr, uid, ids, context=context)		
		self.signal_proforma_voucher(cr, uid, ids)

	def validate_finish(self, cr, uid, ids, context=None):
		self.validate_voucher(cr, uid, ids, context=context)
		return self.close_receipt(cr, uid, ids, context=context)

	def validate_and_new_dialog(self, cr, uid, ids, context=None):
		self.validate_voucher(cr, uid, ids, context=context)
		return self.new_payment(cr, uid, ids, context=context)		
	
	def validate_and_new_normal(self, cr, uid, ids, context=None):
		self.validate_voucher(cr, uid, ids, context=context)
		return self.new_payment(cr, uid, ids, context=context)		

# TODO add on context if dialog or normal
	def new_payment(self, cr, uid, ids, context=None):
		receipt_obj = self.pool['account.voucher.receipt']
		recipt = self.browse(cr, uid, ids[0], context=context).receipt_id
		if not recipt:
			return True
		return receipt_obj.new_payment(cr, uid, [recipt.id], context=context)

	def create_or_add_receipt(self, cr, uid, ids, context=None):
		res = {}
		for record in self.browse(cr, uid, ids, context=context):
			if not record.receipt_id and not context.get('default_receipt_id',False):
				receipt_vals = {
					'partner_id': record.partner_id.id,
					'type': record.type, 
					'receiptbook_id': record.receiptbook_id.id, 	
					'origin_voucher_id': record.id, 	
					'manual_prefix': record.receiptbook_id.manual_prefix,			
				}
				receipt_id = self.pool['account.voucher.receipt'].create(cr, uid, receipt_vals, context=context)
				res[record.id] = receipt_id
				self.write(cr, uid, record.id, {'receipt_id':receipt_id}, context=context)
			else:
				res[record.id] = record.receipt_id.id
		return res
