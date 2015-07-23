# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class account_voucher_line(models.Model):

    _inherit = "account.voucher.line"

    move_line_id = fields.Many2one(
        ondelete='cascade'
        )
