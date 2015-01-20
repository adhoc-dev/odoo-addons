# -*- coding: utf-8 -*-
from openerp import fields, models, api


class account_voucher_populate_statement(models.TransientModel):
    _name = "account.voucher.populate.statement"
    _description = "Account Voucher Populate Statement"

    journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        required=True
    )
    line_ids = fields.Many2many(
        'account.voucher',
        'account_voucher_line_rel_',
        'voucher_id', 'line_id',
        'Vouchers',
        domain="[('journal_id', '=', journal_id), ('state', '=', 'posted'), ('bank_statement_line_ids', '=', False)]"
    )
    
    def get_statement_line_new(self, cr, uid, voucher, statement, context=None):
        # Override thi method to modifiy the new statement line to create
        ctx = context.copy()
        ctx['date'] = voucher.date
        amount = self.pool.get('res.currency').compute(cr, uid, voucher.currency_id.id,
                                                       statement.currency.id, voucher.amount, context=ctx)

        sign = voucher.type == 'payment' and -1.0 or 1.0
        type = voucher.type == 'payment' and 'supplier' or 'customer'
        account_id = voucher.type == 'payment' and voucher.partner_id.property_account_payable.id or voucher.partner_id.property_account_receivable.id
        return {
            'name': voucher.reference or voucher.number or '?',
            'amount': sign * amount,
            'type': type,
            'partner_id': voucher.partner_id.id,
            'account_id': account_id,
            'statement_id': statement.id,
            'ref': voucher.name,
            'voucher_id': voucher.id,
            'journal_entry_id': voucher.move_id.id,
        }

    def populate_statement(self, cr, uid, ids, context=None):
        statement_obj = self.pool.get('account.bank.statement')
        statement_line_obj = self.pool.get('account.bank.statement.line')
        voucher_obj = self.pool.get('account.voucher')

        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        voucher_ids = data['line_ids']
        if not voucher_ids:
            return {'type': 'ir.actions.act_window_close'}
        statement = statement_obj.browse(
            cr, uid, context['active_id'], context=context)
        for voucher in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            statement_line_obj.create(cr, uid,
                                      self.get_statement_line_new(cr, uid, voucher, statement, context=context), context=context)
        voucher_obj.write(
            cr, uid, voucher_ids, {'is_bank_voucher': True}, context=context)
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
