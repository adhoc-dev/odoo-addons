# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class partner(models.Model):
    _inherit = "res.partner"

    sale_require_origin = fields.Boolean(string='Sale Require Origin')
