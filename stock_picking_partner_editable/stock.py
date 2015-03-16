# -*- coding: utf-8 -*-
from openerp import models, fields


class stock_picking(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one(
        states={'cancel': [('readonly', True)]})
