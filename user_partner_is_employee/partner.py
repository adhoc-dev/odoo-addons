# -*- coding: utf-8 -*-
from openerp import fields, models, api


class partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('user_ids.groups_id')
    def _get_is_employee(self):
        is_employee = False
        if self.user_ids:
            is_employee = self.user_ids.user_has_groups('base.group_user')
        self.is_employee = is_employee

    is_employee = fields.Boolean(
        compute='_get_is_employee', string='Is Employee?',
        readonly=True, store=True,
        help="If user belongs to employee group return True",)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
