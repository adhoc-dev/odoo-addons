# -*- coding: utf-8 -*-
from openerp.osv import osv


class account_voucher(osv.osv):

    _inherit = "account.voucher"

    def basic_onchange_partner(
            self, cr, uid, ids, partner_id, journal_id, ttype, context=None):
        res = super(account_voucher, self).basic_onchange_partner(
            cr, uid, ids, partner_id, journal_id, ttype, context=context)
        journal_pool = self.pool.get('account.journal')
        res = {'value': {'account_id': False}}
        if journal_id:
            journal = journal_pool.browse(cr, uid, journal_id, context=context)
            if ttype == 'receipt':
                account_id = journal.default_debit_account_id.id or journal.default_credit_account_id.id
            elif ttype == 'payment':
                account_id = journal.default_credit_account_id.id or journal.default_debit_account_id.id
            res['value']['account_id'] = account_id
        return res
