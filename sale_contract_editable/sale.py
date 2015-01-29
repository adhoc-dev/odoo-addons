#-*- coding:utf-8 -*-
from openerp import models, fields


class sale_order(models.Model):
    _inherit = "sale.order"

    project_id = fields.Many2one(states={}, readonly=False)
