# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning


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
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Payment can not be validated before this date',
        )
    to_pay_amount = fields.Float(
        'To Pay Amount',
        compute='_get_to_pay_amount',
        digits=dp.get_precision('Account'),
        help='Amount To be Paid',
    )

    @api.one
    @api.depends('writeoff_amount')
    def _get_to_pay_amount(self):
        """In v9 should be calculated from debit and credit but can be used now
        because of old onchanges
        IMPORTANTE: We can not make it works when voucher is already saved.
        The correct value is displayed after save in that case"""
        # Can not use this way because old api
        # debit = sum([x.amount for x in self.line_cr_ids])
        # credit = sum([x.amount for x in self.line_dr_ids])
        # balance_amount = debit - credit
        to_pay_amount = self.amount - self.writeoff_amount
        self.to_pay_amount = to_pay_amount

    @api.multi
    def proforma_voucher(self):
        """Make two things:
        * Check payment date valididy
        * Fix not date on voucher error, set actual date.
        """
        for voucher in self:
            if not voucher.date:
                voucher.date = fields.Date.context_today(self)
            if voucher.payment_date > fields.Date.context_today(self):
                raise Warning(_('You can not validate a Voucher that has\
                    Payment Date before Today'))
        return super(account_voucher, self).proforma_voucher()

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
