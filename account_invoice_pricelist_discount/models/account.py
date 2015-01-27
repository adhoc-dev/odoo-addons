# -*- coding: utf-8 -*-
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class sale_order_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    def _get_list_price(self):
        list_price = 0.0
        if self.product_id.list_price:
            list_price = self.with_context(
                currency_id=self.invoice_id.currency_id.id
            ).product_id.price_get()[self.product_id.id]
        self.list_price = list_price

    list_price = fields.Float(
        compute='_get_list_price',
        digits_compute=dp.get_precision('Account'),
        string='List Price')
