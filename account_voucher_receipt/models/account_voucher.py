# -*- coding: utf-8 -*-
from openerp import models, fields, api


class account_voucher(models.Model):

    _inherit = "account.voucher"

    receipt_id = fields.Many2one(
        'account.voucher.receipt',
        string='Receipt',
        required=False,
        readonly=True,
        copy=False,
        )
    receipt_state = fields.Selection(
        related='receipt_id.state',
        string='Receipt State',
        )
    move_ids = fields.One2many(
        related='move_id.line_id',
        # relation='account.move.line',
        string='Journal Items',
        readonly=True
        )

    @api.multi
    def cancel_voucher(self):
        ''' Mofication of cancel voucher so it cancels the receipts when
        voucher is cancelled'''

        res = super(account_voucher, self).cancel_voucher()
        for voucher in self:
            if voucher.receipt_id and voucher.receipt_id.state != 'draft':
                voucher.receipt_id.cancel_receipt()
        return res

    @api.multi
    def action_cancel_draft(self):
        res = super(account_voucher, self).action_cancel_draft()
        for voucher in self:
            if voucher.receipt_id:
                voucher.receipt_id.action_cancel_draft()
        return res
