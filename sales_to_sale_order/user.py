# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, fields, models

class sale_order(models.Model):
    _inherit = 'res.users'

    new_sale_order_user_id = fields.Many2one(
        'res.users',
        'New Sale Order User',
        help="When selecting sale orders and creating a new one, \
            this user will be used for the sale order")
