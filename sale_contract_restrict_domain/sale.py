#-*- coding:utf-8 -*-
from openerp import models, fields


class sale_order(models.Model):
    _inherit = "sale.order"

    commercial_partner_id = fields.Many2one(
        'res.partner',
        string='Commercial Entity',
        related='partner_id.commercial_partner_id',
        store=True,
        readonly=True)
