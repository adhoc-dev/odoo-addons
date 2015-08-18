# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class sale_order(models.Model):
    _inherit = "sale.order"

    sale_require_origin = fields.Boolean(
        string='Sale Require Origin',
        related='partner_id.sale_require_origin')
