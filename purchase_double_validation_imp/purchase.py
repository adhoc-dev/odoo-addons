# -*- coding: utf-8 -*-
from openerp.osv import osv


class purchase_order(osv.osv):

    _inherit = "purchase.order"

    def print_order(self, cr, uid, ids, context=None):
        '''
        This function prints the request for order
        '''
        # assert len(ids) == 1, 'This option should only be used for a single id at a time'
        # wf_service = netsvc.LocalService("workflow")
        # wf_service.trg_validate(uid, 'purchase.order', ids[0], 'send_rfq', cr)
        datas = {
                 'model': 'purchase.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'purchase.order', 'datas': datas, 'nodestroy': True}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
