# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class account_voucher(models.Model):

    _inherit = "account.voucher"

    net_amount = fields.Float(
        'Net Amount',
        digits=dp.get_precision('Account'),
        )
    withholding_amount = fields.Float(
        'Withholdings Amount',
        digits=dp.get_precision('Account'),
        )
    # TODO ver si cambiamos el string de "amount"
    amount = fields.Float(
        string='Total Amount'
        )
    withholding_ids = fields.One2many(
        'account.voucher.withholding',
        'voucher_id',
        string='Withholdings',
        required=False,
        readonly=True,
        states={'draft': [('readonly', False)]}
        )

    @api.model
    def first_move_line_get(
            self, voucher_id, move_id, company_currency, current_currency):
        res = super(account_voucher, self).first_move_line_get(
            voucher_id, move_id, company_currency, current_currency)
        print 'bbbbbbbbbbbbbbbbbbbb'
        print 'bbbbbbbbbbbbbbbbbbbb'
        return res

    @api.model
    def voucher_move_line_create(
            self, voucher_id, line_total, move_id, company_currency,
            current_currency):
        print 'aaaaaaaaaaaaaaaaaaaa'
        print 'aaaaaaaaaaaaaaaaaaaa'
        res = super(account_voucher, self).voucher_move_line_create(
            voucher_id, line_total, move_id, company_currency,
            current_currency)
        return res

    # @api.one
    # def add_withholding(self):
    #     """For each withholding_ids (withholding) it creates an
    #     account.move.line with:
    #         Partner: withholding voucher partner
    #         Account: withholding tax_withholding_id account
    #         Debit/credit: withholding amount
    #     """
    #     return None
