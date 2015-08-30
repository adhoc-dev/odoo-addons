# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class crm_opportunity2phonecall(osv.osv_memory):

    """Converts Opportunity to Phonecall"""
    _inherit = 'crm.opportunity2phonecall'

    _columns = {
        'type_id': fields.many2one(
            'crm.phonecall.type',
            'Type',),
    }

    def action_schedule(self, cr, uid, ids, context=None):
        # value = {}
        if context is None:
            context = {}
        phonecall = self.pool.get('crm.phonecall')
        opportunity_ids = context and context.get('active_ids') or []
        opportunity = self.pool.get('crm.lead')
        data = self.browse(cr, uid, ids, context=context)[0]
        call_ids = opportunity.schedule_phonecall(
            cr, uid, opportunity_ids, data.date, data.name,
            data.note, data.phone, data.contact_name, data.user_id and data.user_id.id or False,
            data.section_id and data.section_id.id or False,
            data.categ_id and data.categ_id.id or False,
            action=data.action, context=context)
        if data.type_id:
            phonecall.write(
                cr, uid, call_ids.values(),
                {'type_id': data.type_id.id}, context=context)
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
