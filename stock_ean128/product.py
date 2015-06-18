# -*- coding: utf-8 -*-
from openerp import models, api


class product_product(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(
            self, name, args=None, operator='ilike',
            limit=100):
        res = super(product_product, self).name_search(
            name, args=args, operator=operator, limit=limit)
        if len(res) < limit:
            products = self.env['stock.production.lot'].search(
                [('ean_128', operator, name)],
                limit=limit).mapped('product_id')
            res += products.name_get()
        return res
