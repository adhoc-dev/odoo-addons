# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning
import openerp.addons.decimal_precision as dp


class AccountAccount(models.Model):
    _inherit = 'account.account'

    restrict_balance = fields.Boolean(
        'Restrict Balance?',
        digits=dp.get_precision('Account'),
        )
    min_balance = fields.Float(
        'Minimum Balance',
        digits=dp.get_precision('Account'),
        )


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def validate(self):
        """We check that there is enaught balance.
        If we want to make this check only on post, we should
        overwrite post method"""
        for move in self:
            for line in move.line_id.filtered('account_id.restrict_balance'):
                if line.account_id.balance < line.account_id.min_balance:
                    raise Warning(_('Can not create move as account %s balance would be %s and account has restriction of min balance to %s') % (
                        line.account_id.name,
                        line.account_id.balance,
                        line.account_id.min_balance))
        return super(AccountMove, self).validate()
