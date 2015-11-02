# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class sale_order(models.Model):
    _inherit = 'sale.order'

    internal_notes = fields.Text('Internal Notes')

    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent,
        so that we can see more easily the next step of the workflow
        '''
        assert len(
            ids) == 1, 'This option should only be used for a single id at a time'
        # self.signal_quotation_sent(cr, uid, ids)
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        report_obj = self.pool.get('ir.actions.report.xml')
        report_name = report_obj.get_report_name(
            cr, uid, 'sale.order', ids, context=context)

        return self.pool['report'].get_action(
            cr, uid, ids, report_name, context=context)

    @api.model
    def _prepare_invoice(self, order, lines):
        vals = super(sale_order, self)._prepare_invoice(order, lines)
        if 'comment' in vals:
            vals.pop('comment')
        vals.update({
            'internal_notes': order.internal_notes})
        return vals
