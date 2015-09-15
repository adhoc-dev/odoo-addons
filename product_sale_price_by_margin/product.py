# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class product_product(models.Model):
    _inherit = "product.template"

    @api.one
    @api.depends('sale_margin', 'sale_surcharge',
                 'product_variant_ids.replenishment_cost')
    def update_list_price(self):
        if len(self.product_variant_ids) > 1:
            replenishment_cost = self.product_variant_ids[0].replenishment_cost
        else:
            replenishment_cost = self.product_variant_ids.replenishment_cost
        self.list_price = replenishment_cost * \
            (1 + self.sale_margin) + self.sale_surcharge

    sale_margin = fields.Float(
        'Sale margin', digits=(16, 4), default=0)
    sale_surcharge = fields.Float(
        'Sale surcharge', digits=dp.get_precision('Product Price'))
    list_price = fields.Float(compute='update_list_price', store=True)
    replenishment_cost_copy = fields.Float(
        related='product_variant_ids.replenishment_cost')
