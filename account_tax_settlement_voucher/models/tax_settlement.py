# -*- coding: utf-8 -*-
from openerp import api, models


class account_tax_settlement(models.Model):
    _inherit = 'account.tax.settlement'

    @api.multi
    def settlement_pay(self):
        self.ensure_one()
        return self.move_id.with_context(
            from_settlement=True).create_voucher('payment')
