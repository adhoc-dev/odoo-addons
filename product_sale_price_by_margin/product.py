# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class product_product(models.Model):
    _inherit = "product.product"
    lst_price = fields.Float(
        readonly=True
        )


class product_template(models.Model):
    _inherit = "product.template"

    @api.one
    @api.depends(
        'sale_margin',
        'sale_surcharge',
        'replenishment_cost',
        'manual_list_price',
        'list_price_type',
        # 'product_variant_ids.replenishment_cost'
        )
    def get_list_price(self):
        if self.list_price_type == 'manual':
            self.list_price = self.manual_list_price
        else:
            self.list_price = self.replenishment_cost * \
                (1 + self.sale_margin / 100.0) + self.sale_surcharge

    sale_margin = fields.Float(
        'Sale margin %',
        digits=dp.get_precision('Discount'),
        )
    sale_surcharge = fields.Float(
        'Sale surcharge',
        digits=dp.get_precision('Product Price')
        )
    list_price_type = fields.Selection([
        ('by_margin', 'By Margin'),
        ('manual', 'Manual'),
        ],
        string='Sale Price Type',
        required=True,
        default='manual',
        )
    manual_list_price = fields.Float(
        'Sale Price',
        digits=dp.get_precision('Product Price'),
        help="Base price to compute the customer price. Sometimes called the "
        "catalog price."
        )
    list_price = fields.Float(
        compute='get_list_price',
        store=True,
        readonly=True,
        )
    replenishment_cost_copy = fields.Float(
        related='product_variant_ids.replenishment_cost'
        )
