# -*- coding: utf-8 -*-
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    def _get_list_price(self):
        price_get = self.with_context(
            currency_id=self.order_id.pricelist_id.currency_id.id
        ).product_id.price_get()
        self.list_price = price_get and price_get[self.product_id.id] or 0.0

    list_price = fields.Float(
        compute='_get_list_price',
        digits_compute=dp.get_precision('Product Price'),
        string='List Price')
