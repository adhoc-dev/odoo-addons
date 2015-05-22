# -*- coding: utf-8 -*-
from openerp import models, fields


class stock_picking(models.Model):
    _inherit = 'stock.production.lot'

    moves_ids = fields.One2many(
        'stock.move', 'restrict_lot_id', string="Moves")
