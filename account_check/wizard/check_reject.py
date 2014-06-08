# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) 2012 OpenERP - Team de Localización Argentina.
# https://launchpad.net/~openerp-l10n-ar-localization
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
from openerp.tools.translate import _
import time

class account_check_dreject(osv.osv_memory):
    _name = 'account.check.dreject'

    _columns = {
        'type': fields.char('Check Type'),
        'state': fields.char('Check State'),
        'reject_date': fields.date('Reject Date', required=True),
        'expense_account': fields.many2one('account.account','Expense Account', domain=[('type','in',['other','liquidity'])],),
        'has_expense': fields.boolean('Has Expense'),
        'expense_amount': fields.float('Expense Amount'),
        'expense_to_customer': fields.boolean('Invoice Expenses to Customer'),
    }

    _defaults = {
        'has_expense': True, 
        'reject_date': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def action_dreject(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        record_ids = context.get('active_ids', [])
        check_obj = self.pool.get('account.check')

        wizard = self.browse(cr, uid, ids[0], context=context)        

        for check in check_obj.browse(cr, uid, record_ids, context=context):
            if check.state not in ['deposited', 'handed']:
                raise osv.except_osv('Check %s selected error' % (check.name),
                    'Only deposited or handed checks can be rejected.')

            if check.type == 'third':
                customer_invoice_id = self.make_invoice(cr, uid, 'out_invoice', check, wizard, context=context)
                if wizard.has_expense and wizard.expense_to_customer:
                    self.make_expense_invoice_line(cr, uid, customer_invoice_id, check, wizard, context=context)
                elif wizard.has_expense:
                    self.make_expenses_move(cr, uid, check, wizard, context=context)
            
            if check.state == 'handed':
                supplier_invoice_id = self.make_invoice(cr, uid, 'in_invoice', check, wizard, context=context)
                if wizard.has_expense:
                    self.make_expense_invoice_line(cr, uid, supplier_invoice_id, check, wizard, context=context)
            check.signal_workflow('rejected')

    def make_expense_invoice_line(self, cr, uid, invoice_id, check, wizard, context=None):
        invoice_line_obj = self.pool.get('account.invoice.line')
        name = _('Rejected Expenses, Check N: ') + check.name
        invoice_line_obj.create(cr, uid, {
            'name': name,
            'origin': name,
            'invoice_id': invoice_id,
            'account_id': wizard.expense_account.id,
            'price_unit': wizard.expense_amount,
            'quantity': 1,
        })       

    def make_invoice(self, cr, uid, invoice_type, check, wizard, context=None):

        if not context:
            context={}
        invoice_line_obj = self.pool.get('account.invoice.line')
        invoice_obj = self.pool.get('account.invoice')
        if invoice_type == 'in_invoice':
            debit_note_field = 'supplier_reject_debit_note_id'
            partner_id = check.destiny_partner_id.id
            partner_account_id = check.voucher_id.partner_id.property_account_payable.id
            account_id = check.voucher_id.journal_id.default_credit_account_id.id
        else:
            debit_note_field = 'customer_reject_debit_note_id'
            partner_account_id = check.voucher_id.partner_id.property_account_receivable.id
            partner_id = check.voucher_id.partner_id.id
            if check.state == 'handed':
                account_id = check.voucher_id.journal_id.default_credit_account_id.id
            else:
                account_id = check.deposit_account_id.id

        name = _('Check Rejected N: ') 
        name += check.name
        invoice_vals = {
            'name': name,
            'origin': name,
            'type': invoice_type,
            'account_id': partner_account_id,
            'partner_id': partner_id,
            'date_invoice': wizard.reject_date,
            }

        invoice_id = invoice_obj.create(cr, uid, invoice_vals, context={'journal_subtype':'debit_note'})
        check.write({debit_note_field: invoice_id})

        invoice_line_vals = {
            'name': name,
            'origin': name,
            'invoice_id': invoice_id,
            'account_id': account_id,
            'price_unit': check.amount,
            'quantity': 1,
        }

        invoice_line_obj.create(cr, uid, invoice_line_vals)

        return invoice_id

    def make_expenses_move(self, cr, uid, check, wizard, context=None):
        move_line_obj = self.pool.get('account.move.line')
        period_id = self.pool.get('account.period').find(cr, uid,wizard.reject_date)[0]
        name = self.pool.get('ir.sequence').next_by_id(cr, uid, check.voucher_id.journal_id.sequence_id.id, context=context)
        ref = _('Check Rejected N: ') 
        ref += check.name
        move_id = self.pool.get('account.move').create(cr, uid, {
            'name': name,
            'journal_id': check.voucher_id.journal_id.id,
            'period_id': period_id,
            'date': wizard.reject_date,
            'ref': _('Rejected Check Nr. ') + check.name,
        })

        move_line_obj.create(cr, uid, {
            'name': name,
            'centralisation': 'normal',
            'account_id': wizard.expense_account.id,
            'move_id': move_id,
            'period_id': period_id,
            'debit': wizard.expense_amount,
            'ref': ref,
        })

        if check.state == 'handed':
            account_id = check.voucher_id.journal_id.default_credit_account_id.id
        else:
            account_id = check.deposit_account_id.id        
        move_line_obj.create(cr, uid, {
            'name': name,
            'centralisation': 'normal',
            'account_id': account_id,
            'move_id': move_id,
            'period_id': period_id,
            'credit': wizard.expense_amount,
            'ref': ref,
        })
        self.pool.get('account.move').write(cr, uid, [move_id], {
            'state': 'posted',
        })
        check.write({'expense_account_move_id': move_id})        