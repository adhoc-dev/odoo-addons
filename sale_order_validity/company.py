# -*- coding: utf-8 -*-
from openerp import fields, models


class res_company(models.Model):
    _inherit = "res.company"

    sale_order_validity_days = fields.Integer(
        'Sale Order Vailidty Period',
        help='Set days of validity for Sales Order, if null, no validity date will be filled')
