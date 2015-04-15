# -*- coding: utf-8 -*-
from openerp import fields, models, api


class product_template(models.Model):
    _inherit = 'product.template'

    can_modify_prices = fields.Boolean(
        help='If checked all users can modify the\
        price of this product in a sale order or invoice.',
        string='Can modify prices')
