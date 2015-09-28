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
    cia_currency_list_price = fields.Float(
        'Company Currency Sale Price',
        digits=dp.get_precision('Product Price'),
        compute='get_cia_currency_list_price',
        help="Base price on company currency at actual exchange rate",
        )

    @api.multi
    @api.depends('list_price', 'sale_price_currency_id')
    def get_cia_currency_list_price(self):
        company_currency = self.env.user.company_id.currency_id
        for product in self:
            if (
                    product.sale_price_currency_id and
                    product.sale_price_currency_id != company_currency
                    ):
                cia_currency_list_price = (
                    product.sale_price_currency_id.compute(
                        product.list_price, company_currency))
            else:
                cia_currency_list_price = product.list_price
            product.cia_currency_list_price = cia_currency_list_price

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
