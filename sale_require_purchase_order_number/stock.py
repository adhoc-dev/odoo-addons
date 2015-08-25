# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class stock_picking(models.Model):
    _inherit = "stock.picking"

    require_purchase_order_number = fields.Boolean(
        string='Sale Require Origin',
        related='partner_id.require_purchase_order_number')
    purchase_order_number = fields.Char(
        'Purchase Order Number',
        states={'cancel': [('readonly', True)],
                'done': [('readonly', True)]})
