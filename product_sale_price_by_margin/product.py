# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class product_product(models.Model):
    _inherit = "product.product"

    @api.one
    @api.depends('sale_margin', 'sale_surcharge', 'replenishment_cost')
    def update_list_price(self):
        self.lst_price = self.replenishment_cost * \
            (1 + self.sale_margin) + self.sale_surcharge

    sale_margin = fields.Float(
        'Sale margin', digits=(16, 4), default=0)
    sale_surcharge = fields.Float(
        'Sale surcharge', digits=dp.get_precision('Product Price'))
    lst_price = fields.Float(compute='update_list_price', store=True)
    replenishment_cost_copy = fields.Float(related='replenishment_cost')
