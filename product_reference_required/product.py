# -*- coding: utf-8 -*-
from openerp import models, fields


class product_product(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(
        required=True,
        )
