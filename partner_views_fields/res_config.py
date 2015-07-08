# -*- coding: utf-8 -*-
from openerp import fields, models


class partner_configuration(models.TransientModel):
    _inherit = 'base.config.settings'

    group_ref = fields.Boolean(
        "Show Reference On Partners Tree View",
        implied_group='partner_views_fields.group_ref',
        )
    group_user_id = fields.Boolean(
        "Show Commercial On Partners Tree View",
        implied_group='partner_views_fields.group_user_id',
        )
    group_city = fields.Boolean(
        "Show City On Partners Tree and Search Views",
        implied_group='partner_views_fields.group_city',
        )
    group_state_id = fields.Boolean(
        "Show State On Partners Tree and Search Views",
        implied_group='partner_views_fields.group_state_id',
        )
    group_country_id = fields.Boolean(
        "Show Country On Partners Tree and Search Views",
        implied_group='partner_views_fields.group_country_id',
        )
    group_function = fields.Boolean(
        "Show Function On Partners Tree and Search Views",
        implied_group='partner_views_fields.group_function',
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
