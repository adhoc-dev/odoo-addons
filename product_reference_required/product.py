# -*- coding: utf-8 -*-
from openerp import models, fields


class product_template(models.Model):
    _inherit = "product.template"

    default_code = fields.Char(
        required=True,
        )


class product_product(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(
        required=True,
        )
