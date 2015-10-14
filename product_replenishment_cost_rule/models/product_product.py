# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    replenishment_cost_rule_id = fields.Many2one(
        'product.replenishment_cost.rule',
        string='Replenishment Cost Rule',
        )

    # @api.one
    @api.depends(
        'replenishment_base_cost',
        # because of being stored
        'replenishment_base_cost_currency_id.rate_ids.rate',
        # and this if we change de date (name field)
        'replenishment_base_cost_currency_id.rate_ids.name',
        # rule items
        'replenishment_cost_rule_id.item_ids.sequence',
        'replenishment_cost_rule_id.item_ids.percentage_amount',
        'replenishment_cost_rule_id.item_ids.fixed_amount',
        )
    def _get_replenishment_cost(self):
        self.replenishment_cost = self.get_replenishment_cost()

    @api.multi
    def get_replenishment_cost(self):
        print '2222222222'
        cost = super(ProductTemplate, self).get_replenishment_cost()
        print 'cost', cost
        if self.replenishment_cost_rule_id:
            for line in self.replenishment_cost_rule_id.item_ids:
                cost = cost * \
                    (1 + line.percentage_amount / 100.0) + line.fixed_amount
                print 'cost', cost
        return cost
    #     from_currency = self.replenishment_base_cost_currency_id
    #     to_currency = self.replenishment_cost_currency_id
    #     from_amount = self.replenishment_base_cost
    #     if from_currency and to_currency:
    #         if from_currency != to_currency:
    #             replenishment_cost = from_currency.compute(
    #                     from_amount, to_currency)
    #         else:
    #             replenishment_cost = from_amount
    #         self.replenishment_cost = replenishment_cost
