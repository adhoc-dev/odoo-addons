# -*- coding: utf-8 -*-
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class sale_order_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    def _get_list_price(self):
        price_get = self.with_context(
            currency_id=self.invoice_id.currency_id.id
        ).product_id.price_get()
        list_price = price_get and price_get[self.product_id.id] or 0.0
        discount = list_price and (
            (list_price - self.price_unit) * 100.0 / list_price) or 0.0
        total_discount = discount + self.discount - (
            discount * self.discount or 0.0) / 100.0

        self.list_price = list_price
        self.list_discount = discount
        self.total_discount = total_discount

    list_price = fields.Float(
        compute='_get_list_price',
        digits_compute=dp.get_precision('Account'),
        string='List Price')
    list_discount = fields.Float(
        compute='_get_list_price',
        string='List Discount')
    total_discount = fields.Float(
        compute='_get_list_price',
        string='Total Discount')
