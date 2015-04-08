# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class account_voucher(models.Model):

    _inherit = "account.voucher"

    balance_amount = fields.Float(
        'Balance Amount',
        compute='_get_balance_amount',
        digits=dp.get_precision('Account'),
        help='Differents between credits and debits to be cancelled.',
    )

# NOTA no esta facil el asunto este porque no se computa bien el writeoff_amount
    def onchange_line_ids(
            self, cr, uid, ids, line_dr_ids, line_cr_ids, amount,
            voucher_currency, type, context=None):
        res = super(account_voucher, self).onchange_line_ids(
            cr, uid, ids, line_dr_ids, line_cr_ids, amount, voucher_currency,
            type, context=None)
        print 'res', res
        if res.get('value') and res.get('value').get('writeoff_amount'):
            res['balance_amount'] = amount - res.get('value').get('writeoff_amount')
        print 'res', res
        return res

    @api.one
    # @api.depends(
    #     'line_cr_ids',
    #     'line_cr_ids.amount',
    #     'line_dr_ids',
    #     'line_dr_ids.amount',
    #     )
    # @api.depends('writeoff_amount')
    def _get_balance_amount(self):
        """In v9 should be calculated from debit and credit but can be used now
        because of old onchanges"""
        # Can not use this way because old api
        # debit = sum([x.amount for x in self.line_cr_ids])
        # credit = sum([x.amount for x in self.line_dr_ids])
        # balance_amount = debit - credit
        balance_amount = self.amount - self.writeoff_amount
        self.balance_amount = balance_amount
