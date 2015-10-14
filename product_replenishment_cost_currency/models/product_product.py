# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # @api.model
    # def get_currency_id(self):
    #     price_type_obj = self.env['product.price.type']
    #     price_type_ids = price_type_obj.search(
    #         [('field', '=', 'replenishment_cost')])
    #     if not price_type_ids.currency_id:
    #         return self.env.user.company_id.currency_id
    #     return price_type_ids.currency_id

    # TODO ver si implementamos o no
    # replenishment_cost_type = fields.Selection([
    #     ('cost', 'Cost'),
    #     ('rep...', 'Cost'),
    #     ]
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
    replenishment_cost_currency_id = fields.Many2one(
        'res.currency',
        'Replenishment Cost Currency',
        compute='get_replenishment_cost_currency_id',
        )

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
        print '1111111'
        self.replenishment_cost = self.get_replenishment_cost()

    @api.multi
    def get_replenishment_cost(self):
        self.ensure_one()
        from_currency = self.replenishment_base_cost_currency_id
        to_currency = self.replenishment_cost_currency_id
        replenishment_cost = self.replenishment_base_cost
        if from_currency and to_currency:
            if from_currency != to_currency:
                replenishment_cost = from_currency.compute(
                        replenishment_cost, to_currency)
        return replenishment_cost
