# -*- coding: utf-8 -*-
from openerp import models


class sale_order(models.Model):
    _inherit = 'sale.order'

    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent,
        so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        # self.signal_quotation_sent(cr, uid, ids)
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        report_obj = self.pool.get('ir.actions.report.xml')
        report_name = report_obj.get_report_name(
            cr, uid, 'sale.order', ids, context=context)

        return self.pool['report'].get_action(
            cr, uid, ids, report_name, context=context)
