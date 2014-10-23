# -*- coding: utf-8 -*-
from openerp import models, fields


class product_template(models.Model):
    _inherit = 'product.template'
    other_sale_description = fields.Char(
        'Other Sale Description',
        help="If this field is set, then on sale orders lines this description will be used and no code.")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
