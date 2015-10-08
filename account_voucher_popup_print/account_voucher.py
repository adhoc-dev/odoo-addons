# -*- coding: utf-8 -*-
from openerp import api, models


class account_voucher(models.Model):
    _inherit = 'account.voucher'

    @api.multi
    def button_register_and_print(self):
        self.ensure_one()
        # register/confirm
        self.button_proforma_voucher()
        return self.receipt_print()
