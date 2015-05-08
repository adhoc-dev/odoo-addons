# -*- coding: utf-8 -*-
from openerp import models, fields


class account_voucher_line(models.Model):

    _inherit = "account.voucher.line"

    move_line_id = fields.Many2one(
        ondelete='cascade'
        )
