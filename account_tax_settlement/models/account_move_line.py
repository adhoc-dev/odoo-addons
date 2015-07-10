# -*- coding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import Warning


class account_move_line(models.Model):
    _inherit = 'account.move.line'

    tax_settlement_detail_id = fields.Many2one(
        'account.tax.settlement.detail',
        'Tax Settlement Detail',
        )
