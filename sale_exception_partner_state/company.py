# -*- coding: utf-8 -*-
from openerp import models, fields


class res_company(models.Model):
    _inherit = "res.company"

    restrict_sales = fields.Selection(
        [('yes', 'Yes'), ('amount_depends', 'Depends on the amount')],
        'Restrict Sales?',
        help="Restrict Sales to Unapproved Partners?"
        )
    restrict_sales_amount = fields.Float(
        'Restrict Amounts Greater Than'
        )
