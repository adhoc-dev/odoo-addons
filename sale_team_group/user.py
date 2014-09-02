# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class res_users(osv.osv):
    _inherit = 'res.users'
    _columns = {
        'section_ids': fields.one2many(
            'crm.case.section',
            'user_id',
            'Equipos de venta a cargo'),
        'sections_id': fields.many2many(
            'crm.case.section',
            'sale_member_rel',
            'member_id',
            'section_id',
            'Equipos de venta a los que pertenece')
    }
