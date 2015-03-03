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
        related='journal_id.check_type', string='Check Type', readonly=True,
        )
    amount_readonly = fields.Float(
        related='amount', string='Total',
        digits_compute=dp.get_precision('Account'), readonly=True,
        )

    @api.multi
    def action_cancel_draft(self):
        res = super(account_voucher, self).action_cancel_draft()
        checks = self.env['account.check'].search(
            [('voucher_id', 'in', self.ids)])
        checks.action_cancel_draft()
        return res

    # def first_move_line_get(self):
    @api.model
    def first_move_line_get(
            self, voucher_id, move_id, company_currency,
            current_currency):
        vals = super(account_voucher, self).first_move_line_get(
            voucher_id, move_id, company_currency, current_currency)
        voucher = self.browse(voucher_id)
        if company_currency != current_currency and voucher.amount:
            debit = vals.get('debit')
            credit = vals.get('credit')
            total = debit - credit
            exchange_rate = total / voucher.amount
            checks = []
            if voucher.check_type == 'third':
                checks = voucher.received_third_check_ids
            elif voucher.check_type == 'issue':
                checks = voucher.issued_check_ids
            for check in checks:
                company_currency_amount = abs(check.amount * exchange_rate)
                check.company_currency_amount = company_currency_amount
        return vals

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

    def onchange_journal(
            self, cr, uid, ids, journal_id, line_ids, tax_id,
            partner_id, date, amount, ttype, company_id, context=None):
        '''
        Override the onchange_journal function to check which are the page and fields that should be shown
        in the view.
        '''
        check_type = False
        validate_only_checks = False
        ret = super(account_voucher, self).onchange_journal(
            cr, uid, ids, journal_id, line_ids, tax_id, partner_id,
            date, amount, ttype, company_id, context=context)
        if not ret:
            ret = {}
        if 'value' not in ret:
            ret['value'] = {}
        if journal_id:
            journal_obj = self.pool.get('account.journal')
            journal = journal_obj.browse(cr, uid, journal_id, context=context)
            if ids:
                for voucher in self.browse(cr, uid, ids, context=context):
                    if voucher.delivered_third_check_ids or voucher.received_third_check_ids or voucher.issued_check_ids:
                        # todo, este warning deberia sumarse a los warnings que
                        # pueden venir en ret['warning']
                        warning = {
                            'title': _('Check Error!'),
                            'message': _('You can not change the journal if there are checks')
                        }
                        ret['warning'] = warning
                        ret['value']['journal_id'] = voucher.journal_id.id

                        # so that check_type is readed ok later
                        journal = voucher.journal_id
            else:
                ret['value']['delivered_third_check_ids'] = False
                ret['value']['received_third_check_ids'] = False
                ret['value']['issued_check_ids'] = False
            validate_only_checks = journal.validate_only_checks
            check_type = journal.check_type
        ret['value']['check_type'] = check_type
        ret['value']['validate_only_checks'] = validate_only_checks
        return ret

    @api.one
    @api.onchange('amount_readonly')
    def onchange_amount_readonly(self):
        self.amount = self.amount_readonly

    @api.one
    @api.onchange('received_third_check_ids', 'issued_check_ids')
    def onchange_customer_checks(self):
        self.amount_readonly = sum(
            x.amount for x in self.received_third_check_ids)

    @api.one
    @api.onchange('delivered_third_check_ids', 'issued_check_ids')
    def onchange_supplier_checks(self):
        amount = sum(x.amount for x in self.delivered_third_check_ids)
        amount += sum(x.amount for x in self.issued_check_ids)
        self.amount_readonly = amount
