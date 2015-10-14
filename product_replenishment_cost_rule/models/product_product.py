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
        cost = super(ProductTemplate, self).get_replenishment_cost()
        if self.replenishment_cost_rule_id:
            for line in self.replenishment_cost_rule_id.item_ids:
                cost = cost * \
                    (1 + line.percentage_amount / 100.0) + line.fixed_amount
        return cost
