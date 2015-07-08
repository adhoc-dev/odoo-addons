# -*- coding: utf-8 -*-
from openerp import fields, api, models


class account_voucher(models.Model):
    _inherit = 'account.voucher'

    tax_move_line_ids = fields.One2many(
        'account.move.line',
        compute='_get_tax_move_lines',
        string='Tax Journal Items',
        # related='move_id.line_id',
        # domain=[('tax_code_id', '!=', False)],
        )
    # tax_move_line_ids = fields.One2many(
        # 'account.move.line',
        # domain=[('tax_code_id', '!=', False)],
        # )

    @api.one
    @api.depends(
        'move_id.line_id.tax_code_id',
        'move_id.line_id.tax_amount',
        )
    def _get_tax_move_lines(self):
        self.tax_move_line_ids = self.move_id.line_id.filtered(
            lambda r: r.tax_code_id and r.tax_amount)
