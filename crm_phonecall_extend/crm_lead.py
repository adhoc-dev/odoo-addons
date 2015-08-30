# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class crm_lead(osv.osv):
    _inherit = "crm.lead"

    def _get_phonecall(self, cr, uid, ids, name, args, context=None):
        result = {}
        phonecall_obj = self.pool['crm.phonecall']
        for lead in self.browse(cr, uid, ids, context=context):
            phonecall_id = False
            type_id = False
            user_id = False
            phonecall_date = False
            phonecall_ids = phonecall_obj.search(cr, uid, [(
                'opportunity_id', '=', lead.id),
                ('state', 'in', ('open', 'pending'))],
                order='date asc', context=context)
            if phonecall_ids:
                phonecall = phonecall_obj.browse(
                    cr, uid, phonecall_ids[0], context=context)
                type_id = phonecall.type_id.id
                user_id = phonecall.user_id.id
                phonecall_date = phonecall.date
            result[lead.id] = {
                'next_phonecall_id': phonecall_id,
                'phonecall_type_id': type_id,
                'phonecall_user_id': user_id,
                'phonecall_date': phonecall_date,
            }
        return result

    _columns = {
        'next_phonecall_id': fields.function(
            _get_phonecall,
            type='many2one',
            string='Next Phonecall',
            multi="call",
            relation='crm.phonecall'),
        'phonecall_date': fields.function(
            _get_phonecall,
            type='datetime',
            string='Phonecall Date',
            multi="call",),
        'phonecall_type_id': fields.function(
            _get_phonecall,
            type='many2one',
            string='Phonecall Type',
            multi="call",
            relation='crm.phonecall.type'),
        'phonecall_user_id': fields.function(
            _get_phonecall,
            type='many2one',
            string='Phonecall Responsible',
            multi="call",
            relation='res.users'),
    }
