# -*- coding: utf-8 -*-
from openerp import api, fields, models

class res_company(models.Model):
    _inherit = 'res.company'

    sale_order_dummy_confirm = fields.Boolean('Sale Orders Dummy Confirmation')