# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class res_company(models.Model):

    """"""

    _inherit = 'res.company'

    default_uom_prices = fields.Boolean(
        string="Default uom price",
        help="When choosing a product , brings the default measurement unit list price UOM")
