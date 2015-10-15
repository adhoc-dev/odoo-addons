# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields
import openerp.addons.decimal_precision as dp


class ProductReplenishmentCostRule(models.Model):
    _name = 'product.replenishment_cost.rule'
    _description = 'product.replenishment_cost.rule'

    name = fields.Char(
        'Name',
        required=True,
        )
    item_ids = fields.One2many(
        'product.replenishment_cost.rule.item',
        'replenishment_cost_rule_id',
        'Items',
        )
    product_ids = fields.One2many(
        'product.template',
        'replenishment_cost_rule_id',
        'Products',
        )


class ProductReplenishmentCostRuleItem(models.Model):
    _name = 'product.replenishment_cost.rule.item'
    _description = 'product.replenishment_cost.rule.item'
    _order = 'sequence'

    replenishment_cost_rule_id = fields.Many2one(
        'product.replenishment_cost.rule',
        'Rule',
        required=True,
        ondelete='cascade',
        )
    sequence = fields.Char(
        'sequence',
        default=10,
        )
    name = fields.Char(
        'Name',
        required=True,
        )
    percentage_amount = fields.Float(
        'Percentage Amount',
        digits=dp.get_precision('Discount'),
        )
    fixed_amount = fields.Float(
        'Fixed Amount',
        digits=dp.get_precision('Product Price'),
        help='Specify the fixed amount to add or substract(if negative) to the'
        ' amount calculated with the percentage amount.'
        )
