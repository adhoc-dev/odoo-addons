# -*- coding: utf-8 -*-
from openerp import fields, models, api


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.one
    def _get_pricelist_discount(self):
        discount = 0.0
        if self.product_id.list_price:
            list_price = self.with_context(
                currency_id=self.order_id.pricelist_id.currency_id.id
            ).product_id.price_get()[self.product_id.id]
            discount = (list_price - self.price_unit) * 100.0 / list_price

        total_discount = discount + self.discount - (
            discount * self.discount or 0.0)
        self.pricelist_discount = discount
        self.total_discount = total_discount

    pricelist_discount = fields.Float(
        compute='_get_pricelist_discount',
        string='Pricelist Discount')

    total_discount = fields.Float(
        compute='_get_pricelist_discount',
        string='Total Discount')
