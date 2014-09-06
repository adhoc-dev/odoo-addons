# -*- coding: utf-8 -*-
from openerp import fields, models, api


class product_product(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _get_user_can_modify(self):
        self.user_can_modify_prices = self.env[
            'res.users'].has_group('price_security.can_modify_prices')

    can_modify_prices = fields.Boolean(
        help='If checked all users can modify the \
        price of this product in a sale order or invoice.',
        string='Can modify prices')
    user_can_modify_prices = fields.Boolean(
        compute='_get_user_can_modify',
        string='User Can modify prices')
