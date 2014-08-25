# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _

class partner_configuration(osv.osv_memory):
    _inherit = 'base.config.settings'

    _columns = {
        'group_vat': fields.boolean("Show VAT On Partners Tree View",
            implied_group='partner_views_fields_base_vat.group_vat',),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
