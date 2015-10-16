# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    replenishment_base_cost = fields.Float(
        'Replenishment Base Cost',
        digits=dp.get_precision('Product Price'),
        help="Replanishment Cost expressed in 'Replenishment Base Cost "
        "Currency'."
        )
    replenishment_base_cost_currency_id = fields.Many2one(
        'res.currency',
        'Replenishment Base Cost Currency',
        help="Currency used for the Replanishment Base Cost."
        )
    # for now we make replenshiment cost field only on template and not in
    # product
    replenishment_cost = fields.Float(
        compute='_get_replenishment_cost',
        string='Replenishment Cost',
        store=True,
        digits=dp.get_precision('Product Price'),
        help="The cost that you have to support in order to produce or "
             "acquire the goods. Depending on the modules installed, "
             "this cost may be computed based on various pieces of "
             "information, for example Bills of Materials or latest "
             "Purchases."
             )
    standard_price_currency_id = fields.Many2one(
        'res.currency',
        'Cost Price Currency',
        compute='get_standard_price_currency',
        )
    replenishment_cost_currency_id = fields.Many2one(
        'res.currency',
        'Replenishment Cost Currency',
        compute='get_replenishment_cost_currency_id',
        )

    @api.one
    def get_standard_price_currency(self):
        price_type = self.env['product.price.type'].search(
            [('field', '=', 'standard_price')], limit=1)
        self.standard_price_currency_id = price_type.currency_id

    @api.one
    def get_replenishment_cost_currency_id(self):
        price_type = self.env['product.price.type'].search(
            [('field', '=', 'replenishment_cost')], limit=1)
        self.replenishment_cost_currency_id = price_type.currency_id

    @api.one
    @api.depends(
        'replenishment_base_cost',
        # because of being stored
        'replenishment_base_cost_currency_id.rate_ids.rate',
        # and this if we change de date (name field)
        'replenishment_base_cost_currency_id.rate_ids.name',
        )
    def _get_replenishment_cost(self):
        self.replenishment_cost = self.get_replenishment_cost_currency()

    @api.multi
    def get_replenishment_cost_currency(self):
        self.ensure_one()
        from_currency = self.replenishment_base_cost_currency_id
        to_currency = self.replenishment_cost_currency_id
        replenishment_cost = False
        if from_currency and to_currency:
            replenishment_cost = self.replenishment_base_cost
            if from_currency != to_currency:
                replenishment_cost = from_currency.compute(
                        replenishment_cost, to_currency)
        return replenishment_cost


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # we make it related to prod template because for now we want it only
    # on prod template
    replenishment_cost = fields.Float(
        related='product_tmpl_id.replenishment_cost',
        )
