# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    phonecall_ids = fields.One2many(
        "crm.phonecall", "partner_id", "Phonecalls"
        )
