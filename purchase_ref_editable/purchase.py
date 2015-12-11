# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class purchase_order(models.Model):

    """"""

    _inherit = 'purchase.order'

    partner_ref = fields.Char(states={})
