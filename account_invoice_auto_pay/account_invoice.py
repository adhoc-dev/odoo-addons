# -*- coding: utf-8 -*-
from openerp import models, api


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        res = super(account_invoice, self).invoice_validate()
        for invoice in self:
            if not invoice.residual or invoice.residual == 0.0:
                invoice.reconciled = True
        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
