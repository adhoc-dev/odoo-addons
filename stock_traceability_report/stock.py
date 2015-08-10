# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class stock_picking(models.Model):
    _inherit = 'stock.production.lot'

    @api.one
    def _get_moves(self):
        moves = []
        for quant in self.quant_ids:
            moves.append([move.id for move in quant.history_ids])
        self.move_ids = moves

    move_ids = fields.One2many('stock.move', compute='_get_moves')
