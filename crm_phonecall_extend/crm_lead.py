# -*- coding: utf-8 -*-
from openerp.osv import fields, osv




class crm_lead(osv.osv):
    _inherit = "crm.lead"

    def _get_phonecall(self, cr, uid, ids, name, args, context=None):
        result = {}
        phonecall_obj=self.pool['crm.phonecall']
        for lead in self.browse(cr, uid, ids, context=context):
            phonecall_id = False
            categ_id = False
            user_id = False
            phonecall_ids = phonecall_obj.search(cr, uid, [('opportunity_id', '=', lead.id ),('state', '=', 'pending')], order='date desc', context=context)
            if phonecall_ids:
                phonecall_id = phonecall_ids[0]
                categ_id= phonecall_obj.browse(cr, uid, phonecall_id, context=context).categ_id.id
                user_id = phonecall_obj.browse(cr, uid, phonecall_id, context=context).user_id.id
            result[lead.id] = {
                    'next_phonecall_id': phonecall_id,
                    'phonecall_categ_id': categ_id,
                    'phonecall_user_id': user_id,
                }
        return result
    
    _columns = {

        'next_phonecall_id': fields.function(_get_phonecall,
            type='many2one',string='Next Phonecall', multi="call", relation='crm.lead'
            ),
        'phonecall_categ_id':fields.function(_get_phonecall, type='many2one', string='Category Phonecall',multi="call",relation='crm.lead'),
        'phonecall_user_id':fields.function(_get_phonecall, type='many2one', string='Users Phonecall', multi="call",relation='crm.lead'),

    }
