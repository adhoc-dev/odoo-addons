# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class intercompany_document(osv.osv):
    _name = 'intercompany.document'
    _description = 'Intercompany Document'

    _columns = {
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, ondelete="cascade",),
        'model': fields.selection(
            [('invoice', 'Invoice')], string='Model', required=True),
        'type': fields.selection(
            [('move_auto', 'Move Automatically'),
             ('move_wizard', 'Move With Wizard')
             ],
            string='Type', required=True),
        'destiny_company_id': fields.many2one(
            'res.company', 'Destiny Company',),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
