# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class crm_phonecall2phonecall(osv.osv_memory):
    _inherit = 'crm.phonecall2phonecall'

    _columns = {
        'type_id': fields.many2one(
            'crm.phonecall.type',
            'Type',),
    }

    def action_schedule(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        phonecall = self.pool.get('crm.phonecall')
        phonecall_ids = context and context.get('active_ids') or []
        for this in self.browse(cr, uid, ids, context=context):
            phocall_ids = phonecall.schedule_another_phonecall(
                cr, uid, phonecall_ids, this.date, this.name,
                this.user_id and this.user_id.id or False,
                this.section_id and this.section_id.id or False,
                this.categ_id and this.categ_id.id or False,
                action=this.action, context=context)
            if this.type_id:
                phonecall.write(
                    cr, uid, phocall_ids.values(),
                    {'type_id': this.type_id.id}, context=context)
        return phonecall.redirect_phonecall_view(
            cr, uid, phocall_ids[phonecall_ids[0]], context=context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
