# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import Warning


class account_move_line(models.Model):
    _inherit = 'account.move.line'

    # we leave this if we want payment to be possible from negative tax with negative tax code sign
    # tax_amount_with_sign = fields.Boolean(
    #     'Tax Amount With Sign',
    #     compute='get_tax_amount_with_sign'
    #     )

    # @api.one
    # @api.depends('tax_amount', 'tax_code_id.sign')
    # def get_tax_amount_with_sign(self):
    #     self.tax_amount_with_sign = self.tax_amount * self.tax_code_id.sign
    tax_settlement_residual = fields.Float(
        related='tax_settlement_move_id.payable_residual'
        )

    @api.multi
    def pay_tax_settlement(self):
        self.ensure_one()
        return self.tax_settlement_move_id.with_context(
            from_settlement=True).create_voucher('payment')
    # @api.multi
    # def make_settlement_and_pay_tax(self):
    #     # INTENTOS DE PAGAR DIRECTAMENTE
    #     # self.ensure_one()
    #     # return self.move_id.with_context(
    #     #     move_line_ids=[self.id],
    #     #     account_id=self.account_id.id).create_voucher(
    #     #         'payment', self.env['res.partner'].browse(73))
    #     self.ensure_one()
    #     if self.reconcile_id:
    #         raise Warning(_('Line already reconciled'))
    #     if not self.tax_code_id:
    #         raise Warning(_(
    #             'Settlement only alled for journal items with tax code'))

    #     # get parent tax codes (only parents)
    #     parent_tax_codes_ids = []
    #     parent_tax_code = self.tax_code_id.parent_id
    #     while parent_tax_code:
    #         parent_tax_codes_ids.append(parent_tax_code.id)
    #         parent_tax_code = parent_tax_code.parent_id

    #     # parent_tax_codes_ids = self.
    #     journals = self.env['account.journal'].search([
    #         ('type', '=', 'tax_settlement'),
    #         ('tax_code_id', 'in', parent_tax_codes_ids),
    #         ])

    #     if not journals:
    #         raise Warning(_(
    #             'No tax settlemnt journal found for tax code %s') % (
    #             self.tax_code_id.name))
    #     elif len(journals) != 1:
    #         raise Warning(_(
    #             'Only one tax settlemnt journal must exist for tax code %s'
    #             'We have found the journal ids %s') % (
    #             self.tax_code_id, journals.ids))
    #     else:
    #         journal = journals

    #     # check account payable
    #     if self.debit < self.credit:
    #         account = journal.default_debit_account_id
    #         tax_code = journal.default_debit_tax_code_id
    #     else:
    #         account = journal.default_credit_account_id
    #         tax_code = journal.default_credit_tax_code_id

    #     # check account type so that we can create a debt
    #     if account.type != 'payable':
    #         raise Warning(_(
    #             'You can only pay if tax counterpart use a payable account.'
    #             'Account id %i' % account.id))

    #     # get date, period and name
    #     date = fields.Date.context_today(self)
    #     period = self.env['account.period'].with_context(
    #         company_id=self.company_id.id).find(date)[:1]
    #     name = journal.sequence_id._next()

    #     move_vals = {
    #         # 'ref': self.name,
    #         'name': name,
    #         'period_id': period.id,
    #         'date': date,
    #         'journal_id': journal.id,
    #         'company_id': self.company_id.id,
    #         }
    #     move = self.env['account.move'].create(move_vals)

    #     counterpart_line_vals = {
    #         'move_id': move.id,
    #         'partner_id': self.partner_id.id,
    #         'name': self.name,
    #         'debit': self.credit,
    #         'credit': self.debit,
    #         'account_id': self.account_id.id,
    #         'tax_code_id': self.tax_code_id.id,
    #         'tax_amount': self.tax_amount,
    #     }
    #     counterpart_line = move.line_id.create(counterpart_line_vals)

    #     # TODO ver si ref se completa con el name del journal
    #     deb_line_vals = {
    #         'move_id': move.id,
    #         'partner_id': journal.partner_id.commercial_partner_id.id,
    #         'name': self.name,
    #         'debit': self.debit,
    #         'credit': self.credit,
    #         'account_id': account.id,
    #         'tax_code_id': tax_code.id,
    #         'tax_amount': -1.0 * self.tax_amount,
    #     }
    #     move.line_id.create(deb_line_vals)
    #     (counterpart_line + self).reconcile_partial()
    #     return move.create_voucher('payment')
