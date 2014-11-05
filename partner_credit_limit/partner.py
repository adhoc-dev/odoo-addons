# -*- coding: utf-8 -*-
from openerp import fields, models, api


class res_partner(models.Model):
    _inherit = 'res.partner'

    user_edit_credit_limit = fields.Boolean(
        "Edit Credit Limit On Customers",
        compute="_get_user_edit_credit_limit",
        )

    @api.one
    def _get_user_edit_credit_limit(self):
        self.user_edit_credit_limit = self.env[
            'res.users'].has_group('partner_credit_limit.credit_config')
