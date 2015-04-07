# -*- coding: utf-8 -*-
from openerp import models, fields, _, api
import openerp.addons.decimal_precision as dp
import logging
from openerp.exceptions import Warning
_logger = logging.getLogger(__name__)


class account_voucher(models.Model):

    _inherit = 'account.voucher'

    received_third_check_ids = fields.One2many(
        'account.check', 'voucher_id', 'Third Checks',
        domain=[('type', '=', 'third')],
        context={'default_type': 'third', 'from_voucher': True},
        required=False, readonly=True, copy=False,
        states={'draft': [('readonly', False)]}
        )
    issued_check_ids = fields.One2many(
        'account.check', 'voucher_id', 'Issued Checks',
        domain=[('type', '=', 'issue')],
        context={'default_type': 'issue', 'from_voucher': True}, copy=False,
        required=False, readonly=True, states={'draft': [('readonly', False)]}
        )
    delivered_third_check_ids = fields.One2many(
        'account.check', 'third_handed_voucher_id',
        'Third Checks', domain=[('type', '=', 'third')], copy=False,
        context={'from_voucher': True}, required=False, readonly=True,
        states={'draft': [('readonly', False)]}
        )
    validate_only_checks = fields.Boolean(
        related='journal_id.validate_only_checks',
        string='Validate only Checks', readonly=True,
        )
    check_type = fields.Selection(
        related='journal_id.check_type',
        string='Check Type', readonly=True,
        )
    dummy_journal_id = fields.Many2one(
        related='journal_id', readonly=True,
        string='Dummy Journa',
        help='Field used for new api onchange methods over journal',
        )
    amount_readonly = fields.Float(
        related='amount', string='Total',
        digits_compute=dp.get_precision('Account'), readonly=True,
        )

    @api.onchange('dummy_journal_id')
    def change_dummy_journal_id(self):
        """Unlink checks on journal change"""
        self.delivered_third_check_ids = False
        self.issued_check_ids = False
        self.received_third_check_ids = False

    @api.multi
    def action_cancel_draft(self):
        res = super(account_voucher, self).action_cancel_draft()
        checks = self.env['account.check'].search(
            [('voucher_id', 'in', self.ids)])
        checks.action_cancel_draft()
        return res

    @api.multi
    def cancel_voucher(self):
        for voucher in self:
            for check in voucher.received_third_check_ids:
                if check.state not in ['draft', 'holding']:
                    raise Warning(_(
                        'You can not cancel a voucher thas has received third checks in states other than "draft or "holding". First try to change check state.'))
            for check in voucher.issued_check_ids:
                if check.state not in ['draft', 'handed']:
                    raise Warning(_(
                        'You can not cancel a voucher thas has issue checks in states other than "draft or "handed". First try to change check state.'))
            for check in voucher.delivered_third_check_ids:
                if check.state not in ['handed']:
                    raise Warning(_(
                        'You can not cancel a voucher thas has delivered checks in states other than "handed". First try to change check state.'))
        res = super(account_voucher, self).cancel_voucher()
        checks = self.env['account.check'].search([
            '|',
            ('voucher_id', 'in', self.ids),
            ('third_handed_voucher_id', 'in', self.ids)])
        for check in checks:
            check.signal_workflow('cancel')
        return res

    def proforma_voucher(self, cr, uid, ids, context=None):
        res = super(account_voucher, self).proforma_voucher(
            cr, uid, ids, context=None)
        for voucher in self.browse(cr, uid, ids, context=context):
            if voucher.type == 'payment':
                for check in voucher.issued_check_ids:
                    check.signal_workflow('draft_router')
                for check in voucher.delivered_third_check_ids:
                    check.signal_workflow('holding_handed')
            elif voucher.type == 'receipt':
                for check in voucher.received_third_check_ids:
                    check.signal_workflow('draft_router')
        return res

    @api.one
    @api.onchange(
        'received_third_check_ids',
        'delivered_third_check_ids',
        'issued_check_ids'
        )
    def onchange_checks(self):
        """We force the update of paylines and amount"""
        self._get_paylines_amount()
        self._get_amount()

    @api.multi
    def get_paylines_amount(self):
        res = super(account_voucher, self).get_paylines_amount()
        for key, value in res.iteritems():
            new_val = value
            new_val += sum(x.amount for x in self.received_third_check_ids)
            new_val += sum(x.amount for x in self.delivered_third_check_ids)
            new_val += sum(x.amount for x in self.issued_check_ids)
            res[key] = new_val
        return res

# TODO ver si borramos el amount readonly
    @api.model
    def paylines_moves_create(
            self, voucher, move_id, company_currency, current_currency):
        move_lines = self.env['account.move.line']
        paylines_total = super(account_voucher, self).paylines_moves_create(
            voucher, move_id, company_currency, current_currency)
        if voucher.check_type == 'third':
            if voucher.type == 'payment':
                checks = voucher.delivered_third_check_ids
            else:
                checks = voucher.received_third_check_ids
        elif voucher.check_type == 'issue':
            checks = voucher.issued_check_ids
        # Calculate total
        paylines_total = 0.0
        for check in checks:
            bank_name = ''
            if check.bank_id:
                bank_name = '/' + check.bank_id.name
            check_move_line = move_lines.create(
                self.prepare_check_move_line(
                    voucher, check.amount, move_id, check.name + bank_name,
                    company_currency, current_currency, check.payment_date))
            paylines_total += check_move_line.debit - check_move_line.credit
        return paylines_total

    @api.model
    def prepare_check_move_line(
            self, voucher, amount, move_id, name, company_currency,
            current_currency, date_due):
    # TODO convertir de otra manera el monto, usando una funcion que existe para tal fin
        exchange_rate = voucher.paid_amount_in_company_currency / voucher.amount
        debit = credit = 0.0
        if voucher.type in ('purchase', 'payment'):
            credit = amount * exchange_rate
        elif voucher.type in ('sale', 'receipt'):
            debit = amount * exchange_rate
        if debit < 0: credit = -debit; debit = 0.0
        if credit < 0: debit = -credit; credit = 0.0
        sign = debit - credit < 0 and -1 or 1
        move_line = {
                'name': name,
                'debit': debit,
                'credit': credit,
                'account_id': voucher.account_id.id,
                'move_id': move_id,
                'journal_id': voucher.journal_id.id,
                'period_id': voucher.period_id.id,
                'partner_id': voucher.partner_id.id,
                'currency_id': company_currency <> current_currency and  current_currency or False,
                'amount_currency': (sign * abs(amount) # amount < 0 for refunds
                    if company_currency != current_currency else 0.0),
                'date': voucher.date,
                'date_maturity': date_due or False,
            }
        return move_line
