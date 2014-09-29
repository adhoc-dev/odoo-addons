# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp.tools.translate import _

class generate_pairkey(osv.osv_memory):
        _name = 'crypto.generate_pairkey'

        _columns = {
            'name': fields.char('Pair key name', size=63),
            'key_length': fields.integer('Key lenght'),
            'update': fields.boolean('Update key'),
        }

        _defaults = {
            'key_length': 1024,
        }

        def on_generate(self, cr, uid, ids, context):
            if context is None:
                context = {}
            active_ids = context['active_ids']
            pairkey_obj = self.pool.get('crypto.pairkey')
            for wizard in self.browse(cr, uid, ids):
                pairkey_obj.generate_keys(cr, uid, active_ids, key_length=wizard.key_length)
                pairkey_obj.action_validate(cr, uid, active_ids)
            return {'type': 'ir.actions.act_window_close'}

        def on_cancel(self, cr, uid, ids, context):
            return {}

generate_pairkey()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
