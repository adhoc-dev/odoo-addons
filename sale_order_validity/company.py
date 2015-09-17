# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class res_company(models.Model):
    _inherit = "res.company"

    sale_order_validity_days = fields.Integer(
        'Sale Order Validity Days',
        help='Set days of validity for Sales Order, if null, no validity date '
        'will be filled')
