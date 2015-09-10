# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def get_currency_id(self):
        price_type_obj = self.env['product.price.type']
        price_type_ids = price_type_obj.search(
            [('field', '=', 'replenishment_cost')])
        if not price_type_ids.currency_id:
            return self.env.user.company_id.currency_id
        return price_type_ids.currency_id

    currency_replenishment_cost = fields.Float(
        'Currency Replanishment Cost',
        digits=dp.get_precision('Product Price'),
        help="Replanishment Cost expressed in 'Replanishment Cost Currency'."
        )
    replenishment_cost_currency_id = fields.Many2one(
        'res.currency',
        'Replanishment Cost Currency',
        default=get_currency_id,
        help="Currency used for the Replanishment Cost."
        )
    replenishment_cost = fields.Float(
        related='product_variant_ids.replenishment_cost',
        string='Replenishment Cost'
        )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.one
    @api.depends(
        'product_tmpl_id.standard_price',
        'product_tmpl_id.replenishment_cost_currency_id',
        'product_tmpl_id.currency_replenishment_cost',
        # because of being stored
        'product_tmpl_id.replenishment_cost_currency_id.rate_ids.rate',
        'product_tmpl_id.replenishment_cost_currency_id.rate_ids.name',
        )
    def _get_replenishment_cost(self):
        # to_currency is price_type or user company currency
        to_currency = self.product_tmpl_id.get_currency_id()
        cost_currency = self.product_tmpl_id.replenishment_cost_currency_id
        currency_cost = self.product_tmpl_id.currency_replenishment_cost
        if cost_currency and currency_cost:
            if cost_currency != to_currency:
                replenishment_cost = cost_currency.compute(
                        currency_cost, to_currency)
            else:
                replenishment_cost = currency_cost
        else:
            replenishment_cost = self.standard_price
        self.replenishment_cost = replenishment_cost

    replenishment_cost = fields.Float(
        compute=_get_replenishment_cost,
        string='Replenishment Cost',
        )
