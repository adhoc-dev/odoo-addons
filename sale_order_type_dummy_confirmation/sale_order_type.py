# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class SaleOrderTypology(models.Model):
    _inherit = 'sale.order.type'

    dummy_confirm = fields.Boolean(
        'Dummy Confirmation',
        help='If you set True then all orders of this type will be dummy '
        'confirmed. If company has dummy confirm set, then no matter what you '
        'choose here, orders will be dummy confirmed'
        )
