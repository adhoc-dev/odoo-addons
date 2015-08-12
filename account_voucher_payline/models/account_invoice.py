# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class account_invoice(models.Model):

    _inherit = "account.invoice"

    @api.multi
    def invoice_pay_customer(self):
        self.ensure_one()
        res = super(account_invoice, self).invoice_pay_customer()
        res['context']['default_net_amount'] = (
            self.type in ('out_refund', 'in_refund') and -self.residual
            or self.residual)
        return res
