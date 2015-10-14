# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    # product_id = fields.Integer(
    #     related='product_variant_ids.product_id'
    #     # 'product.pricelist',
    #     # compute='_get_product_id',
    #     # store=True
    #     )
    # pricelist_ids = fields.Many2many(
    pricelist_ids = fields.One2many(
        'product.pricelist',
        compute='get_pricelist_ids',
        inverse='dummy_inverse',
        string='Pricelists',
        )

    @api.one
    def dummy_inverse(self):
        """
        Dummy Inverse function so that we can edit vouchers and save changes
        """
        return True

    @api.one
    # TODO use multi
    def get_pricelist_ids(self):
        self.pricelist_ids = self.pricelist_ids.search([])


# class product_product(models.Model):
#     _inherit = 'product.product'

#     # product_id = fields.Many2one(
#     product_id = fields.Integer(
#         # 'product.pricelist',
#         related='id',
#         # compute='_get_product_id',
#         # store=True
#         )
