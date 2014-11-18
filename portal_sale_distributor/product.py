# -*- coding: utf-8 -*-
from openerp import models, fields


class product_template(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(
        groups='base.group_user,base.group_portal_distributor')
