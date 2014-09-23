# -*- coding: utf-8 -*-
from openerp import models, fields


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    declared_value = fields.Float(
        'Declared Value', digits=(16, 2),)
