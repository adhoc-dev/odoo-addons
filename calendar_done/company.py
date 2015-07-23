# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class company(models.Model):
    _inherit = "res.company"

    calendar_mark_done_user_id = fields.Many2one(
        'res.users', string='Calendar Mark Done User')
