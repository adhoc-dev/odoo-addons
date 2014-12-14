# -*- coding: utf-8 -*-
from openerp import fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    phonecall_ids = fields.One2many(
        "crm.phonecall", "partner_id", "Phonecalls"
        )
