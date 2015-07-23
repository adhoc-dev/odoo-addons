# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _
from openerp.exceptions import Warning


class hr_so_project(models.TransientModel):
    _inherit = 'hr.sign.out.project'

    account_id = fields.Many2one(
        domain=[('type', 'in', ['normal', 'contract']),
                ('state', 'in', ['open', 'pending'])]
    )

    @api.onchange('account_id')
    def on_change_account_id(self):
        if self.account_id and self.account_id.state == 'pending':
            raise Warning(
                _('The Analytic Account is pending state!'))
