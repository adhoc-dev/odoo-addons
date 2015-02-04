# -*- coding: utf-8 -*-
from openerp import models, fields


class stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'

    disable_sale_stock_warning = fields.Boolean('Disable Sale Stock Warning')
