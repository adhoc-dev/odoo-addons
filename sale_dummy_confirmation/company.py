# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class res_company(models.Model):
    _inherit = 'res.company'

    sale_order_dummy_confirm = fields.Boolean(
        'Sale Orders Dummy Confirmation',
        help='If you set True then all orders of this company will be dummy '
        'confirmed'
        )
