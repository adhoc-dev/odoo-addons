# -*- coding: utf-8 -*-
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    @api.depends(
        'product_id',
        'discount',
        'price_unit',
        'order_id',
        'order_id.pricelist_id',
        'order_id.pricelist_id.currency_id',
        )
    def _get_list_price(self):
        price_get = self.product_id.with_context(
            currency_id=self.order_id.pricelist_id.currency_id.id
        ).price_get()
        list_price = price_get and price_get[self.product_id.id] or 0.0
        list_discount = list_price and (
            (list_price - self.price_unit) * 100.0 / list_price) or 0.0
        total_discount = list_discount + self.discount - (
            list_discount * self.discount or 0.0) / 100.0

        self.list_price = list_price
        self.list_discount = list_discount
        self.total_discount = total_discount

    @api.one
    def _set_discount(self):
        discount = 0.0
        # if price_unit = 0 then we dont calculate anything
        if self.price_unit:
            total_discount_perc = self.total_discount / 100.0
            list_discount_perc = self.list_discount / 100.0
            discount = 1.0 - ((1.0 - total_discount_perc) / (1.0 - list_discount_perc))
        self.discount = discount * 100.0

    list_price = fields.Float(
        compute='_get_list_price',
        digits_compute=dp.get_precision('Product Price'),
        string='List Price')
    list_discount = fields.Float(
        compute='_get_list_price',
        string='List Discount')
    total_discount = fields.Float(
        compute='_get_list_price',
        inverse='_set_discount',
        string='Total Discount')
