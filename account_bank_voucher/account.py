# -*- coding: utf-8 -*-
from openerp import models, fields, api,  _
from openerp.exceptions import Warning


class account_bank_statement(models.Model):
    _inherit = 'account.bank.statement'

    def button_cancel(self, cr, uid, ids, context=None):
        context['cancel_from_statement'] = True
        return super(account_bank_statement, self).button_cancel(
            cr, uid, ids, context=context)


class account_bank_statement_line(models.Model):
    _inherit = 'account.bank.statement.line'

    voucher_id = fields.Many2one('account.voucher', 'Voucher', readonly=True)

    def cancel(self, cr, uid, ids, context=None):
        # if we are canceling the statement then we dont raise the warning
        if context.get('cancel_from_statement', False):
            none_voucher_ids = self.search(
                cr, uid,
                [('id', 'in', ids), ('voucher_id', '=', False)])
            return super(account_bank_statement_line, self).cancel(
                cr, uid, none_voucher_ids, context)

        for line in self.browse(cr, uid, ids, context):
            if line.voucher_id:
                raise Warning(
                    _("You can not cancel a line that has been imported from a Voucher, you should cancel the voucher first"))
        return super(account_bank_statement_line, self).cancel(
            cr, uid, ids, context)

        account_move_obj = self.pool.get('account.move')
        move_ids = []
        for line in self.browse(cr, uid, ids, context=context):
            if line.journal_entry_id:
                move_ids.append(line.journal_entry_id.id)
                for aml in line.journal_entry_id.line_id:
                    if aml.reconcile_id:
                        move_lines = [l.id for l in aml.reconcile_id.line_id]
                        move_lines.remove(aml.id)
                        self.pool.get('account.move.reconcile').unlink(
                            cr, uid, [aml.reconcile_id.id], context=context)
                        if len(move_lines) >= 2:
                            self.pool.get('account.move.line').reconcile_partial(
                                cr, uid, move_lines, 'auto', context=context)
        if move_ids:
            account_move_obj.button_cancel(cr, uid, move_ids, context=context)
            account_move_obj.unlink(cr, uid, move_ids, context)

    def unlink(self, cr, uid, ids, context=None):
        line_voucher_ids = self.search(
            cr, uid,
            [('id', 'in', ids), ('voucher_id', '!=', False)])
        # First remove journal_entry_id id in order to avoid constraint
        self.write(cr, uid, line_voucher_ids, {'journal_entry_id': False})
        return super(account_bank_statement_line, self).unlink(
            cr, uid, ids, context=context)


class account_voucher(models.Model):
    _inherit = 'account.voucher'

    bank_statement_line_ids = fields.One2many(
        'account.bank.statement.line', 'voucher_id', string="Statement Lines")

    @api.multi
    def cancel_voucher(self):
        # run with sudo because some users may not have access to statement line
        if self.sudo().bank_statement_line_ids.statement_id.state == 'confirm':
            raise Warning(
                _("You can not cancel a voucher that is linked to a confirm bank statement"))
        else:
            super(account_voucher, self).cancel_voucher()
            return self.sudo().bank_statement_line_ids.unlink()
