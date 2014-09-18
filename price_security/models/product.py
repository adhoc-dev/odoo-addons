# -*- coding: utf-8 -*-
from openerp import fields, models, api


class product_template(models.Model):
    _inherit = 'product.template'

    can_modify_prices = fields.Boolean(
        help='If checked all users can modify the\
        price of this product in a sale order or invoice.',
        string='Can modify prices')

    @api.multi
    def _get_user_restrict_prices(self):
        self.user_restrict_prices = self.env.user.restrict_prices

    user_restrict_prices = fields.Boolean(
        compute='_get_user_restrict_prices',
        string='User Restrict Prices')
