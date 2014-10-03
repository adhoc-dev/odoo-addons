# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _


class meeting(osv.osv):
    _inherit = "crm.meeting"
    _columns = {
        'mark_done': fields.boolean(string='Mark As Done'),
        'previous_user_id': fields.many2one('res.users', string='Previous User'),
    }

    def on_change_mark_done(self, cr, uid, ids, mark_done, user_id, previous_user_id, context=None):
        vals = {}
        company = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id
        if not company.calendar_mark_done_user_id:
            raise osv.except_osv(_('Error!'), _('You should set the mark done user on the company!',))
        if mark_done:
            vals['user_id'] = company.calendar_mark_done_user_id.id
            vals['previous_user_id'] = user_id
        else:
            vals['user_id'] = previous_user_id
            vals['previous_user_id'] = False
        return {'value': vals}
