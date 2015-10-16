# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class product_template(models.Model):
    _inherit = 'product.template'

    @api.model
    def get_currency_id(self):
        price_type_obj = self.env['product.price.type']
        price_type_ids = price_type_obj.search([('field', '=', 'list_price')])
        if not price_type_ids.currency_id:
            return self.env.user.company_id.currency_id
        return price_type_ids.currency_id

    sale_price_currency_id = fields.Many2one(
        'res.currency', 'Sale Price Currency',
        required=True, default=get_currency_id,
        help="Currency used for the Currency List Price."
        )
    sale_price_on_list_price_type_currency = fields.Float(
        'Sale Price on List Price Currency',
        digits=dp.get_precision('Product Price'),
        compute='get_sale_price_on_list_price_type_currency',
        help="Base price on List Price Type currency at actual exchange rate",
        )
    list_price_type_currency_id = fields.Many2one(
        'res.currency',
        'List Price Type Currency',
        compute='get_sale_price_on_list_price_type_currency',
        )

    @api.one
    @api.depends('list_price', 'sale_price_currency_id')
    def get_sale_price_on_list_price_type_currency(self):
        price_type = self.env['product.price.type'].search(
            [('field', '=', 'list_price')], limit=1)
        to_currency = price_type.currency_id
        self.list_price_type_currency_id = to_currency
        for product in self:
            if (
                    product.sale_price_currency_id and
                    product.sale_price_currency_id != to_currency
                    ):
                to_price = (
                    product.sale_price_currency_id.compute(
                        product.list_price, to_currency))
            else:
                to_price = product.list_price
            product.sale_price_on_list_price_type_currency = to_price

    def _price_get(self, cr, uid, products, ptype='list_price', context=None):
        if not context:
            context = {}
        res = super(product_template, self)._price_get(
            cr, uid, products, ptype=ptype, context=context)
        if ptype == 'list_price':
            pricetype_obj = self.pool.get('product.price.type')
            price_type_id = pricetype_obj.search(
                cr, uid, [('field', '=', ptype)])[0]
            price_type_currency_id = pricetype_obj.browse(
                cr, uid, price_type_id).currency_id.id
            for product in products:
                if product.sale_price_currency_id.id != price_type_currency_id:
                    res[product.id] = self.pool.get('res.currency').compute(
                        cr, uid, product.sale_price_currency_id.id,
                        price_type_currency_id, res[product.id],
                        context=context)
        return res
