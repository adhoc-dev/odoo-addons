# -*- coding: utf-8 -*-
from openerp import fields, models


class company(models.Model):
    _inherit = "res.company"

    calendar_mark_done_user_id = fields.Many2one(
        'res.users', string='Calendar Mark Done User')
