# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class company(osv.osv):
    _inherit = "res.company"
    _columns = {
        'calendar_mark_done_user_id': fields.many2one('res.users', string='Calendar Mark Done User'),
    }
