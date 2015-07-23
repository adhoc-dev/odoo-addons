# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'

    disable_sale_stock_warning = fields.Boolean('Disable Sale Stock Warning')
