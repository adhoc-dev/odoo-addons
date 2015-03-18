# -*- coding: utf-8 -*-
from openerp import fields, models, api


class res_partner(models.Model):
    _inherit = 'res.partner'

    balance = fields.Float(
        compute='_get_balance',
        string='Balance',
        )

    @api.one
    @api.depends('debit', 'credit')
    def _get_balance(self):
        self.balance = self.credit - self.debit

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
