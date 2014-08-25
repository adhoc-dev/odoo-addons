# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _

class partner_configuration(osv.osv_memory):
    _inherit = 'base.config.settings'

    _columns = {
        'group_ref': fields.boolean("Show Reference On Partners Tree View",
            implied_group='partner_views_fields.group_ref',),
        'group_user_id': fields.boolean("Show Commercial On Partners Tree View",
            implied_group='partner_views_fields.group_user_id',),
        'group_city': fields.boolean("Show City On Partners Tree and Search Views",
            implied_group='partner_views_fields.group_city',),
        'group_state_id': fields.boolean("Show State On Partners Tree and Search Views",
            implied_group='partner_views_fields.group_state_id',),
        'group_country_id': fields.boolean("Show Country On Partners Tree and Search Views",
            implied_group='partner_views_fields.group_country_id',),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
