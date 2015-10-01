# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, _, api
import openerp.addons.decimal_precision as dp
import logging
from openerp.exceptions import Warning
_logger = logging.getLogger(__name__)


class account_voucher(models.Model):

    _inherit = 'account.voucher'

    received_third_check_ids = fields.One2many(
        'account.check', 'voucher_id', 'Third Checks',
        domain=[('type', '=', 'third_check')],
        context={'default_type': 'third_check', 'from_voucher': True},
        required=False,
        readonly=True,
        copy=False,
        states={'draft': [('readonly', False)]}
        )
    issued_check_ids = fields.One2many(
        'account.check', 'voucher_id', 'Issued Checks',
        domain=[('type', '=', 'issue_check')],
        context={'default_type': 'issue_check', 'from_voucher': True},
        copy=False,
        required=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    delivered_third_check_ids = fields.One2many(
        'account.check', 'third_handed_voucher_id',
        'Third Checks', domain=[('type', '=', 'third_check')],
        copy=False,
        context={'from_voucher': True},
        required=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    checks_amount = fields.Float(
        _('Amount'),
        compute='_get_checks_amount',
        digits=dp.get_precision('Account'),
        help=_('Amount Paid With Checks'),
    )

    @api.onchange('dummy_journal_id')
    def change_dummy_journal_id(self):
        """Unlink checks on journal change"""
        # if we select checks journal we set net_amount to 0
        if self.journal_id.payment_subtype in ('issue_check', 'third_check'):
            self.net_amount = False
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
        third_handed_checks = self.env['account.check'].search([
            ('third_handed_voucher_id', 'in', self.filtered(
                lambda v: v.type == 'payment').ids)])
        for third_check in third_handed_checks:
            if third_check.state != 'handed':
                raise Warning(_(
                    'You can not cancel handed third checks in states other '
                    'than "handed". First try to change check state.'))
        third_handed_checks.signal_workflow('handed_holding')

        other_checks = self.env['account.check'].search([
            ('voucher_id', 'in', self.ids)])
        other_checks.check_check_cancellation()
        other_checks.signal_workflow('cancel')
        # checks = self.env['account.check'].search([
        #     '|',
        #     ('voucher_id', 'in', self.ids),
        #     ('third_handed_voucher_id', 'in', self.ids)])
        # checks.check_check_cancellation()
        # checks.signal_workflow('cancel')
        return super(account_voucher, self).cancel_voucher()

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
    @api.depends(
        'received_third_check_ids',
        'delivered_third_check_ids',
        'issued_check_ids'
        )
    def _get_checks_amount(self):
        self.checks_amount = self.get_checks_amount()[self.id]
        # We force the update of paylines and amount
        self._get_paylines_amount()
        self._get_amount()

    @api.multi
    def get_checks_amount(self):
        res = {}
        for voucher in self:
            checks_amount = 0.0
            checks_amount += sum(
                x.amount for x in voucher.received_third_check_ids)
            checks_amount += sum(
                x.amount for x in voucher.delivered_third_check_ids)
            checks_amount += sum(
                x.amount for x in voucher.issued_check_ids)
            res[voucher.id] = checks_amount
        return res

    @api.multi
    def get_paylines_amount(self):
        res = super(account_voucher, self).get_paylines_amount()
        for voucher in self:
            checks_amount = voucher.get_checks_amount()[voucher.id]
            res[voucher.id] = res[voucher.id] + checks_amount
        return res

    @api.model
    def paylines_moves_create(
            self, voucher, move_id, company_currency, current_currency):
        paylines_total = super(account_voucher, self).paylines_moves_create(
            voucher, move_id, company_currency, current_currency)
        checks_total = self.create_check_lines(
            voucher, move_id, company_currency, current_currency)
        return paylines_total + checks_total

    @api.model
    def create_check_lines(
            self, voucher, move_id, company_currency, current_currency):
        move_lines = self.env['account.move.line']
        checks = []
        if voucher.payment_subtype == 'third_check':
            if voucher.type == 'payment':
                checks = voucher.delivered_third_check_ids
            else:
                checks = voucher.received_third_check_ids
        elif voucher.payment_subtype == 'issue_check':
            checks = voucher.issued_check_ids
        # Calculate total
        checks_total = 0.0
        for line in checks:
            name = line.name
            if line.bank_id:
                name += '/' + line.bank_id.name
            payment_date = line.payment_date
            amount = line.amount
            account = voucher.account_id
            partner = voucher.partner_id
            move_line = move_lines.create(
                self.prepare_move_line(
                    voucher, amount, move_id, name, company_currency,
                    current_currency, payment_date, account, partner)
                    )
            checks_total += move_line.debit - move_line.credit
        return checks_total
