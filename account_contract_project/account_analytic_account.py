# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    project_id = fields.Many2one(
        'project.project',
        compute='_get_project',
        string=_('Project')
    )

    @api.one
    def _get_project(self):
        self.project_id = self.env['project.project'].search(
            [('analytic_account_id', '=', self.id)], limit=1)
