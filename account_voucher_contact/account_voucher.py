# -*- coding: utf-8 -*-
from openerp import models, api, fields


class account_voucher_line(models.Model):
    _inherit = 'account.voucher.line'

    invoice_partner_id = fields.Many2one(
        'res.partner',
        compute='get_invoice_partner'
        )

    @api.one
    @api.depends('move_line_id')
    def get_invoice_partner(self):
        self.invoice_partner_id = self.move_line_id.invoice.partner_id
