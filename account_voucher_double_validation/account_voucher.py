# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class account_voucher(models.Model):
    _inherit = "account.voucher"

    state = fields.Selection(
        # selection_add=[
        #     ('confirmed', 'Confirmed'),
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancelled'),
            ('proforma', 'Pro-forma'),
            ('posted', 'Posted')
        ])
    # TODO Agregar al help
        # help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Voucher. \
        #             \n* The \'Pro-forma\' when voucher is in Pro-forma status,voucher does not have an voucher number. \
        #             \n* The \'Posted\' status is used when user create voucher,a voucher number is generated and voucher entries are created in account \
        #             \n* The \'Cancelled\' status is used when user cancel voucher.'),
    # partner_id = fields.Many2one('')
    # to_pay_amount = fields.Float(
    #     'To Pay Amount',
    #     digits=dp.get_precision('Account'),
    #     # required=True,
    #     readonly=True,
    #     states={'draft': [('readonly', False)]},
    #     help='Amount To be Paid',
    # )
    net_amount = fields.Float(
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
        )
    journal_id = fields.Many2one(
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
        )
    received_third_check_ids = fields.One2many(
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
        )
    issued_check_ids = fields.One2many(
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
        )
    delivered_third_check_ids = fields.One2many(
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
        )
    withholding_ids = fields.One2many(
        states={'draft': [('readonly', False)],
                'confirmed': [('readonly', False)]}
        )
    date = fields.Date(
        default=False,
        )
    payment_date = fields.Date(
        string='Payment Date',
        readony=True,
        states={'draft': [('readonly', False)]},
        help='Payment can not be validated before this date',
        )

    @api.multi
    def action_move_line_create(self):
        """Fix not date on voucher error, set actual date"""
        for voucher in self:
            if not voucher.date:
                voucher.date = fields.Date.context_today(self)
        return super(account_voucher, self).action_move_line_create()
    # @api.one
    # @api.depends('net_amount', 'type', 'to_pay_amount')
    # def _get_amount(self):
    #     if self.type == 'payment':
    #         amount = self.to_pay_amount
    #     else:
    #         amount = self.paylines_amount + self.net_amount
    #     self.amount = amount

    # TODO si lo usamos para setear el to pay amount
    # @api.one
    # @api.onchange('amount_readonly')
    # def _set_net_amount(self):
    #     super(account_voucher, self)._set_net_amount()
    #     self.to_pay_amount = self.amount

    def onchange_journal(self, cr, uid, ids, journal_id, line_ids, tax_id,
                         partner_id, date, amount, ttype, company_id,
                         context=None):
        if not journal_id:
            return False
        if ids:
            vouchers = self.browse(cr, uid, ids, context=context)
            # Si esta confirmado solo actualizamos la currency y otra data
            if vouchers[0].state == 'confirmed':
                journal_pool = self.pool.get('account.journal')
                journal = journal_pool.browse(
                    cr, uid, journal_id, context=context)
                vals = {'value': {}}
                currency_id = False
                if journal.currency:
                    currency_id = journal.currency.id
                else:
                    currency_id = journal.company_id.currency_id.id

                vals['value'].update({
                    'currency_id': currency_id,
                    'payment_rate_currency_id': currency_id,
                })
                return vals
        return super(account_voucher, self).onchange_journal(
            cr, uid, ids, journal_id, line_ids, tax_id, partner_id, date,
            amount, ttype, company_id, context=context)
