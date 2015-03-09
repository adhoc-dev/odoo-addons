# -*- coding: utf-8 -*-
from openerp import fields, models


class hr_so_project(models.TransientModel):
    _inherit = 'hr.sign.out.project'

    account_id = fields.Many2one(
        domain=[('type', 'in', ['normal', 'contract']), ('state', '=', 'open')]
    )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
