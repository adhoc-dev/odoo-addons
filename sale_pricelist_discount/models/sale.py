# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False):
        res = super(sale_order_line, self).product_id_change(
            pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position,
            flag=flag)
        price_get = self.env['product.product'].browse(product).with_context(
            currency_id=self.env['product.pricelist'].browse(
                pricelist).currency_id.id).price_get()
        if 'value' not in res:
            res['value'] = {}
        res['value']['list_price'] = price_get and price_get[
            product] or False
        return res

    @api.one
    @api.constrains('product_id')
    def set_list_price(self):
        currency = self.order_id.pricelist_id.currency_id
        if self.product_id and currency:
            price_get = self.product_id.with_context(
                currency_id=currency.id
                ).price_get()

            self.list_price = price_get and price_get[
                self.product_id.id] or False

    @api.one
    @api.depends(
        'discount',
        'price_unit',
        )
    def _get_discounts(self):
        list_price = self.list_price
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
            discount = 1.0 - (
                (1.0 - total_discount_perc) / (1.0 - list_discount_perc))
        self.discount = discount * 100.0

    list_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        string='List Price',
        readonly=True
        )
    list_discount = fields.Float(
        compute='_get_discounts',
        string='List Discount'
        )
    total_discount = fields.Float(
        compute='_get_discounts',
        inverse='_set_discount',
        string='Total Discount'
        )
