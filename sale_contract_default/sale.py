# -*- coding: utf-8 -*-
from openerp import models


class account_analytic_account(models.Model):
    _inherit = 'account.analytic.account'

    def _get_one_full_name(self, elmt, level=6):
        res = super(account_analytic_account, self)._get_one_full_name(
            elmt, level)
        if level == 6 and elmt.partner_id:
            res = ('%s - %s') % (res, elmt.partner_id.name)
        return res

    def name_search(
            self, cr, uid, name, args=None,
            operator='ilike', context=None, limit=100):
        res = super(account_analytic_account, self).name_search(
            cr, uid, name, args, operator, context, limit)
        if len(res) < limit:
            account_ids = self.search(
                cr, uid, [('partner_id.name', operator, name)] + args,
                limit=limit, context=context)
            res += self.name_get(cr, uid, account_ids, context=context)
        return res
